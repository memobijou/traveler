from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
# Create your views here.
from infobox.models import Infobox
from supplication.forms import SupplicationDataForm, SupplicationForm, SupplicationVariantForm
from django.db import transaction

from supplication.models import Supplication, SupplicationVariant


class NewSupplicationView(View):
    template_name = "supplication/new_supplication.html"
    form = None
    supplication_form = None

    def get(self, request, **kwargs):
        context = self.get_context()
        return render(request, template_name=self.template_name, context=context)

    def get_context(self):
        infobox = get_object_or_404(Infobox, pk=self.kwargs.get("pk"))
        self.form = self.get_data_form()
        self.supplication_form = self.get_supplication_form()
        context = {"infobox": infobox, "category": infobox.category, "form": self.form,
                   "category_id": infobox.category_id, "supplication_form": self.supplication_form}
        return context

    def get_data_form(self):
        if self.request.POST:
            data_form = SupplicationDataForm(data=self.request.POST, files=self.request.FILES, prefix="data")
        else:
            data_form = SupplicationDataForm(prefix="data")
        return data_form

    def get_supplication_form(self):
        if self.request.POST:
            supplication_form = SupplicationForm(data=self.request.POST, prefix="supplication")
        else:
            supplication_form = SupplicationForm(prefix="supplication")
        return supplication_form

    @transaction.atomic
    def post(self, request, **kwargs):
        context = self.get_context()
        infobox = context.get("infobox")
        if self.form.is_valid() is True and self.supplication_form.is_valid() is True:
            supplication_data = self.form.save()
            supplication = self.supplication_form.save()
            supplication.supplication_data = supplication_data
            supplication.infobox = infobox
            supplication.save()
            return HttpResponseRedirect(reverse_lazy("infobox:edit",
                                                     kwargs={"pk": infobox.pk, "category_id": infobox.category_id}))
        else:
            return render(request, template_name=self.template_name, context=context)


class UpdateSupplicationView(View):
    template_name = "supplication/update_supplication.html"
    form = None
    supplication_form = None

    def get(self, request, **kwargs):
        context = self.get_context()
        return render(request, template_name=self.template_name, context=context)

    def get_context(self):
        infobox = get_object_or_404(Infobox, pk=self.kwargs.get("pk"))
        supplication = get_object_or_404(Supplication, pk=self.kwargs.get("supplication_id"))
        supplication_data = supplication.supplication_data
        self.form = self.get_data_form(supplication_data)
        self.supplication_form = self.get_supplication_form(supplication)
        context = {"infobox": infobox, "category": infobox.category, "form": self.form,
                   "category_id": infobox.category_id, "supplication_form": self.supplication_form,
                   "supplication_data": supplication_data, "supplication": supplication
                   }
        return context

    def get_data_form(self, supplication_data):
        if self.request.POST:
            data_form = SupplicationDataForm(data=self.request.POST, files=self.request.FILES,
                                             instance=supplication_data, prefix="data")
        else:
            data_form = SupplicationDataForm(prefix="data", instance=supplication_data)
        return data_form

    def get_supplication_form(self, supplication):
        if self.request.POST:
            supplication_form = SupplicationForm(data=self.request.POST, instance=supplication, prefix="supplication")
        else:
            supplication_form = SupplicationForm(prefix="supplication", instance=supplication)
        return supplication_form

    @transaction.atomic
    def post(self, request, **kwargs):
        context = self.get_context()
        infobox = context.get("infobox")
        if self.form.is_valid() is True and self.supplication_form.is_valid() is True:
            self.form.save()
            supplication = self.supplication_form.save()
            return HttpResponseRedirect(reverse_lazy("supplication:edit",
                                                     kwargs={"pk": infobox.pk, "supplication_id": supplication.pk}))
        else:
            return render(request, template_name=self.template_name, context=context)


class NewSupplicationVariantView(View):
    template_name = "supplication/new_variant.html"
    form = None
    supplication_variant_form = None

    def get(self, request, **kwargs):
        context = self.get_context()
        return render(request, template_name=self.template_name, context=context)

    def get_context(self):
        infobox = get_object_or_404(Infobox, pk=self.kwargs.get("pk"))
        self.form = self.get_data_form()
        parent_supplication = get_object_or_404(Supplication, pk=self.kwargs.get("supplication_id"))
        self.supplication_variant_form = self.get_supplication_variant_form()
        context = {"infobox": infobox, "category": infobox.category, "category_id": infobox.category_id,
                   "form": self.form, "supplication_form": self.supplication_variant_form,
                   "parent_supplication_data": parent_supplication.supplication_data}
        return context

    def get_data_form(self):
        if self.request.POST:
            data_form = SupplicationDataForm(data=self.request.POST, files=self.request.FILES, prefix="data")
        else:
            data_form = SupplicationDataForm(prefix="data")
        return data_form

    def get_supplication_variant_form(self):
        if self.request.POST:
            supplication_form = SupplicationVariantForm(data=self.request.POST, prefix="supplication")
        else:
            supplication_form = SupplicationVariantForm(prefix="supplication")
        return supplication_form

    @transaction.atomic
    def post(self, request, **kwargs):
        context = self.get_context()
        infobox = context.get("infobox")
        if self.form.is_valid() is True and self.supplication_variant_form.is_valid() is True:
            supplication_data = self.form.save()
            supplication_variant = self.supplication_variant_form.save()
            supplication_variant.supplication_data = supplication_data
            supplication_variant.parent_id = self.kwargs.get("supplication_id")
            supplication_variant.save()
            return HttpResponseRedirect(reverse_lazy("supplication:edit",
                                                     kwargs={"pk": infobox.pk,
                                                             "supplication_id": self.kwargs.get("supplication_id")}))
        else:
            return render(request, template_name=self.template_name, context=context)


class UpdateSupplicationVariantView(View):
    template_name = "supplication/update_variant.html"
    form = None
    supplication_variant_form = None

    def get(self, request, **kwargs):
        context = self.get_context()
        return render(request, template_name=self.template_name, context=context)

    def get_context(self):
        infobox = get_object_or_404(Infobox, pk=self.kwargs.get("pk"))
        supplication_variant = get_object_or_404(SupplicationVariant, pk=self.kwargs.get("supplication_variant_id"))
        parent_supplication = supplication_variant.parent
        parent_supplication_data = parent_supplication.supplication_data
        supplication_variant_data = supplication_variant.supplication_data
        self.form = self.get_data_form(supplication_variant_data)
        self.supplication_variant_form = self.get_supplication_variant_form(supplication_variant)
        context = {"infobox": infobox, "category": infobox.category, "form": self.form,
                   "category_id": infobox.category_id, "supplication_form": self.supplication_variant_form,
                   "supplication_data": supplication_variant_data, "supplication": supplication_variant,
                   "parent_supplication": parent_supplication, "parent_supplication_data": parent_supplication_data
                   }
        return context

    def get_data_form(self, supplication_data):
        if self.request.POST:
            data_form = SupplicationDataForm(data=self.request.POST, files=self.request.FILES,
                                             instance=supplication_data, prefix="data")
        else:
            data_form = SupplicationDataForm(prefix="data", instance=supplication_data)
        return data_form

    def get_supplication_variant_form(self, supplication_variant):
        if self.request.POST:
            supplication_form = SupplicationVariantForm(data=self.request.POST, instance=supplication_variant,
                                                        prefix="supplication")
        else:
            supplication_form = SupplicationVariantForm(prefix="supplication", instance=supplication_variant)
        return supplication_form

    @transaction.atomic
    def post(self, request, **kwargs):
        context = self.get_context()
        infobox = context.get("infobox")
        supplication_parent = context.get("parent_supplication")
        if self.form.is_valid() is True and self.supplication_variant_form.is_valid() is True:
            self.form.save()
            supplication_variant = self.supplication_variant_form.save()
            return HttpResponseRedirect(
                reverse_lazy(
                    "supplication:edit_variant", kwargs={"pk": infobox.pk, "supplication_id": supplication_parent.pk,
                                                         "supplication_variant_id": supplication_variant.id}))
        else:
            return render(request, template_name=self.template_name, context=context)
