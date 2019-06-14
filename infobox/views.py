from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from infobox.models import Category, Infobox
from infobox.forms import CategoryCreationForm, InfoboxCreationForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse


class CategoryView(LoginRequiredMixin, CreateView):
    template_name = "infobox/category.html"
    form_class = CategoryCreationForm

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        if category_id:
            return Category.objects.filter(parent_id=category_id)
        else:
            return Category.objects.filter(parent_id__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        category_id = self.kwargs.get("pk")
        if category_id:
            context["object"] = get_object_or_404(Category, pk=category_id)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        parent_id = self.kwargs.get("pk")
        if parent_id:
            instance.parent_id = parent_id
        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.kwargs.get("pk")
        if category_id:
            return reverse_lazy("infobox:new_category", kwargs={"pk": category_id})
        else:
            return reverse_lazy("infobox:category")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "infobox/edit_category.html"
    form_class = CategoryCreationForm

    def get_object(self, queryset=None):
        return Category.objects.get(pk=self.kwargs.get("pk"))

    def get_success_url(self):
        category_id = self.kwargs.get("pk")
        return reverse_lazy("infobox:edit_category", kwargs={"pk": category_id})


class InfoboxView(LoginRequiredMixin, CreateView):
    form_class = InfoboxCreationForm
    success_url = reverse_lazy("infobox:category")
    template_name = "infobox/new_infobox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        parent = None
        if pk:
            parent = get_object_or_404(Infobox, pk=pk)
            context["parent"] = parent
        context["parent_id"] = pk
        category_id = self.kwargs.get("category_id")
        if category_id:
            context["category_id"] = category_id
            context["category"] = get_object_or_404(Category, pk=category_id)
        else:
            category_id = parent.category_id
            context["category_id"] = category_id
            context["category"] = get_object_or_404(Category, pk=category_id)

        if parent:
            context["is_variant"] = True
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = form.instance
        category_id = self.kwargs.get("category_id")
        infobox_parent_id = self.kwargs.get("pk")

        if infobox_parent_id:
            instance.parent_id = infobox_parent_id
            return form

        if category_id:
            instance.category_id = category_id
        return form

    def get_success_url(self):
        category_id = self.kwargs.get("category_id")
        infobox_parent_id = self.kwargs.get("pk")

        if category_id:
            return reverse_lazy("infobox:edit", kwargs={"pk": self.object.pk, "category_id": category_id})
        else:
            return reverse_lazy("infobox:edit", kwargs={"pk": self.object.pk, "parent_id": infobox_parent_id})


class InfoboxUpdateView(LoginRequiredMixin, UpdateView):
    form_class = InfoboxCreationForm
    template_name = "infobox/edit_infobox.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Infobox, pk=self.kwargs.get("pk"))

    def get_success_url(self):
        if self.object.category_id:
            return reverse_lazy("infobox:edit", kwargs={"pk": self.object.pk, "category_id": self.object.category_id})
        else:
            return reverse_lazy("infobox:edit", kwargs={"pk": self.object.pk, "parent_id": self.object.parent_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_id = self.kwargs.get("parent_id")
        child_id = self.kwargs.get("pk")
        if parent_id:
            parent = get_object_or_404(Infobox, pk=parent_id)
        else:
            print(f"????????????? {child_id}")
            child = get_object_or_404(Infobox, pk=child_id)
            print(f"ho: {child.parent_id}")
            parent = child.parent
        print(f"hey: {parent}")
        context["parent"] = parent
        context["parent_id"] = parent_id
        category_id = self.kwargs.get("category_id")

        if category_id:
            context["category_id"] = category_id
        else:
            category_id = parent.category_id
            context["category_id"] = category_id

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            context["category"] = category

        is_variant = None
        if parent:
            is_variant = True
        context["is_variant"] = is_variant

        if is_variant:
            context["object_list"] = parent.infobox_set.exclude(id=child_id)
        else:
            context["object_list"] = self.object.infobox_set.all()
        return context


class InfoboxDeleteView(generic.View):
    def post(self, request, *args, **kwargs):
        infobox = get_object_or_404(Infobox, pk=self.kwargs.get("pk"))
        if infobox.category:
            category = infobox.category
            infobox.delete()
            return HttpResponseRedirect(reverse_lazy("infobox:new_category", kwargs={"pk": category.pk}))
        else:
            parent = infobox.parent
            category = infobox.parent.category
            infobox.delete()
            return HttpResponseRedirect(
                reverse_lazy("infobox:edit", kwargs={"pk": parent.pk, "category_id": category.id}))


class CategoryDeleteView(generic.View):
    def post(self, request, *args, **kwargs):
        print(f"hallo: {self.request.POST.getlist('item')}")
        categories = Category.objects.filter(pk__in=self.request.POST.getlist("item"))
        categories_with_infoboxes = categories.annotate(
            infoboxes_count=Count("infoboxes")).filter(infoboxes_count__gt=0)
        categories_with_infoboxes_count = categories_with_infoboxes.count()

        if categories_with_infoboxes_count > 0:
            return JsonResponse({"error": "Sie können keine Kategorien mit Infoboxen löschen"}, status=400)

        categories_with_sub_categories = categories.annotate(
            child_categories_count=Count("child_categories")).filter(child_categories_count__gt=0)

        categories_with_sub_categories_count = categories_with_sub_categories.count()

        if categories_with_sub_categories_count > 0:
            return JsonResponse({"error": "Sie können keine Kategorien mit Unterkategorien löschen"}, status=400)

        current_category_parent_id = self.kwargs.get("parent_id")

        categories.delete()

        print(f"??????? {current_category_parent_id}")

        if current_category_parent_id:
            return JsonResponse(
                {"redirect_url": reverse_lazy("infobox:new_category", kwargs={"pk": current_category_parent_id})},
                status=200)
        else:
            return JsonResponse({"redirect_url": reverse_lazy("infobox:category")}, status=200)

