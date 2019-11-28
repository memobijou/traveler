from django import forms

from supplication.models import SupplicationData, Supplication, SupplicationVariant


class SupplicationDataForm(forms.ModelForm):
    class Meta:
        model = SupplicationData
        fields = ("title", "description", "audio", "language", "phonetic_spelling",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            if type(visible.field) != forms.FileField:
                visible.field.widget.attrs["class"] = "form-control"


class SupplicationForm(forms.ModelForm):
    class Meta:
        model = Supplication
        fields = ("type",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            if type(visible.field) != forms.FileField:
                visible.field.widget.attrs["class"] = "form-control"


class SupplicationVariantForm(forms.ModelForm):
    class Meta:
        model = SupplicationVariant
        fields = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for visible in self.visible_fields():
            if type(visible.field) != forms.FileField:
                visible.field.widget.attrs["class"] = "form-control"
