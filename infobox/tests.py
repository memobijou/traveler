from django.test import TestCase
from django.urls import reverse_lazy
from infobox.models import Category, Infobox
from django.contrib.auth.models import User
import json


class InfoboxTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="root", password="root")
        self.client.force_login(self.user)

    def test_category_creation(self):
        title, description = "Category", "Description"
        response = self.client.post(reverse_lazy("infobox:category"),
                                    data={"title": title, "description": description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        category_instance = Category.objects.first()
        self.assertEqual(category_instance.title, title)
        self.assertEqual(category_instance.description, description)

    def test_sub_category_creation(self):
        category = Category.objects.create(title="parent category")
        response = self.client.post(reverse_lazy("infobox:new_category", kwargs={"pk": category.pk},)
                                    , data={"title": "Child category"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.exclude(id=category.id).first().parent_id, category.id)

    def test_category_edition(self):
        new_title = "NEW TITLE"
        category = Category.objects.create(title="category")
        response = self.client.post(reverse_lazy("infobox:edit_category", kwargs={"pk": category.pk}, )
                                    , data={"title": new_title})
        category_instance = Category.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(category_instance.title, new_title)

    def test_infobox_creation(self):
        category = Category.objects.create(title="Category")
        title, description = "Infobox", "description"
        response = self.client.post(reverse_lazy("infobox:new", kwargs={"category_id": category.id}),
                                    data={"title": title, "language": "Deutsch", "description": "description",})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.count(), 1)
        infobox_instance = Infobox.objects.first()
        self.assertEqual(infobox_instance.category, category)
        self.assertEqual(infobox_instance.title, title)
        self.assertEqual(infobox_instance.description, description)
        self.assertEqual(Infobox.objects.count(), 1)

    def test_sub_infobox_creation(self):
        category = Category.objects.create(title="Category")
        infobox_parent = Infobox.objects.create(title="Infobox Parent", language="Deutsch", category_id=category.id)
        response = self.client.post(reverse_lazy(
            "infobox:new", kwargs={"category_id": category.id, "pk": infobox_parent.id}),
            data={"title": "Infobox 2", "language": "Arabisch"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.count(), 2)
        self.assertEqual(Infobox.objects.exclude(id=infobox_parent.id).first().parent_id, infobox_parent.id)

    def test_infobox_edition(self):
        category = Category.objects.create(title="Category")
        data = {"title": "Infobox", "language": "Deutsch"}
        infobox = Infobox.objects.create(**data, category_id=category.id)
        data["title"] = "EDIT"
        response = self.client.post(reverse_lazy("infobox:edit", kwargs={"category_id": category.id, "pk": infobox.pk}),
                                    data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.first().title, "EDIT")

    def test_sub_infobox_edition(self):
        category = Category.objects.create(title="Category")
        infobox_parent = Infobox.objects.create(title="Infobox Parent", language="Deutsch", category_id=category.id)
        infobox_child = Infobox.objects.create(title="Infobox Child", language="Arabisch", parent_id=infobox_parent.id)
        response = self.client.post(reverse_lazy(
            "infobox:edit", kwargs={"parent_id": infobox_parent.id, "pk": infobox_child.id}),
            data={"title": "EDIT", "language": "Arabisch"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.get(id=infobox_child.id).title, "EDIT")

    def test_new_sub_infobox_language_is_unique(self):
        category = Category.objects.create(title="Category")
        infobox_parent = Infobox.objects.create(title="Infobox Parent", language="Deutsch", category_id=category.id)
        infobox_child = Infobox.objects.create(
            title="Infobox Child 1", language="Arabisch", parent_id=infobox_parent.id)
        response = self.client.post(reverse_lazy(
            "infobox:new", kwargs={"category_id": category.id, "pk": infobox_parent.id}),
            data={"title": "Infobox Child 2", "language": "Arabisch"})
        self.assertEqual(response.status_code, 200)  # error Page ist immer 200
        self.assertEqual(Infobox.objects.count(), 2)

    def test_edit_sub_infobox_language_is_unique(self):
        category = Category.objects.create(title="Category")
        infobox_parent = Infobox.objects.create(title="Infobox Parent", language="Deutsch", category_id=category.id)
        infobox_child = Infobox.objects.create(title="Infobox Child", language="Arabisch", parent_id=infobox_parent.id)

        response = self.client.post(reverse_lazy(
            "infobox:edit", kwargs={"parent_id": infobox_parent.id, "pk": infobox_child.id}),
            data={"title": "EDIT", "language": "Deutsch"})
        self.assertEqual(response.status_code, 200)  # error page is rendered as html content

    def test_infobox_deletion(self):
        infobox, _ = self.create_sample_infobox()
        response = self.client.post(
            reverse_lazy("infobox:delete", kwargs={"pk": infobox.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.count(), 0)

    def test_infobox_variant_deletion(self):
        _, infobox_child = self.create_sample_infobox()
        response = self.client.post(
            reverse_lazy("infobox:delete", kwargs={"pk": infobox_child.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Infobox.objects.count(), 1)

    def test_category_deletion(self):
        category = self.create_sample_category()
        response = self.client.post(
            reverse_lazy("infobox:delete_category"), data={"item": [category.pk]})
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("redirect_url", json_response)
        self.assertEqual(Category.objects.count(), 0)

    def test_sub_category_deletion(self):
        child_category = self.create_sample_category()
        parent_category = self.create_sample_category()
        child_category.parent = parent_category
        response = self.client.post(
            reverse_lazy("infobox:delete_category"), data={"item": [child_category.pk]})
        json_response = json.loads(response.content)
        self.assertIn("redirect_url", json_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)

    def test_deletion_of_category_with_infoboxes_fails(self):
        infobox_parent, _ = self.create_sample_infobox()
        category = infobox_parent.category
        response = self.client.post(
            reverse_lazy("infobox:delete_category"), data={"item": [category.pk]})
        self.assertEqual(response.status_code, 400, "Error repsonse should be returned")
        self.assertEqual(Category.objects.count(), 1, "The category should not be deleted")

    def test_deletion_of_category_with_sub_categories_fails(self):
        category_parent = self.create_sample_category()
        category_child = self.create_sample_category()
        category_child.parent = category_parent
        category_child.save()
        response = self.client.post(
            reverse_lazy("infobox:delete_category"), data={"item": [category_parent.pk]})
        self.assertEqual(response.status_code, 400, "Error repsonse should be returned")
        self.assertEqual(Category.objects.count(), 2, "The category should not be deleted")

    def create_sample_infobox(self):
        category = Category.objects.create(title="Category")
        infobox_parent = Infobox.objects.create(title="Infobox Parent", language="Deutsch", category_id=category.id)
        infobox_child = Infobox.objects.create(title="Infobox Child", language="Arabisch", parent_id=infobox_parent.id)
        return infobox_parent, infobox_child

    def create_sample_category(self):
        category = Category.objects.create(title="Category")
        return category

    def test_get_categories_from_rest_api(self):
        self.create_sample_category()
        self.create_sample_category()
        response = self.client.get(reverse_lazy("infobox_api:category-list"))
        json_response = dict(json.loads(response.content))
        print(json_response)
        self.assertEqual(json_response.get("count"), 2)

    def test_get_category_from_rest_api(self):
        category_instance = self.create_sample_category()
        response = self.client.get(reverse_lazy("infobox_api:category-detail", kwargs={"pk": category_instance.pk}))
        json_response = dict(json.loads(response.content))
        print(json_response)
        self.assertEqual(json_response.get("id"), category_instance.pk)
