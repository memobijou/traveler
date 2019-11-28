from django import forms
from infobox.models import Category, Infobox


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("title", "description", )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class InfoboxCreationForm(forms.ModelForm):
    class Meta:
        model = Infobox
        fields = ("language", "title", "description",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            if type(visible.field) != forms.FileField:
                visible.field.widget.attrs["class"] = "form-control"

    def clean_language(self):
        language = self.cleaned_data['language']
        if self.instance.parent_id:
            language_occurence = 0
            if self.instance.pk:
                language_occurence += self.instance.parent.infobox_set.filter(
                    language=language).exclude(pk=self.instance.pk).count()
            else:
                language_occurence += self.instance.parent.infobox_set.filter(language=language).count()
            if language == self.instance.parent.language:
                language_occurence += 1
            if language_occurence > 0:
                self.add_error("language", "Eine Infobox in dieser Sprache ist bereits angelegt")
        return language
