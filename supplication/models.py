from django.db import models
from django.utils.translation import gettext as _


language_choices = (("Arabisch", "Arabisch"), ("Deutsch", "Deutsch"), ("Türkisch", "Türkisch"), ("Urdu", "Urdu"),)
type_choices = (("Mustahabb", "Mustahabb"), ("Sunnah", "Sunnah"))


class Supplication(models.Model):
    type = models.CharField(max_length=200, null=True, blank=True, choices=type_choices, verbose_name=_("Art"))
    infobox = models.ForeignKey("infobox.Infobox", null=True, blank=True, verbose_name=_("Infobox"),
                                on_delete=models.SET_NULL)
    supplication_data = models.OneToOneField("supplication.SupplicationData", null=True, blank=True,
                                             on_delete=models.SET_NULL, verbose_name=_("Stammdaten"))


class SupplicationVariant(models.Model):
    supplication_data = models.OneToOneField("supplication.SupplicationData", null=True, blank=True,
                                             on_delete=models.SET_NULL, verbose_name=_("Stammdaten"))
    parent = models.ForeignKey("supplication.Supplication", null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name=_("Parent"))


class SupplicationData(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Bezeichnung"))
    description = models.TextField(verbose_name=_("Beschreibung"), null=True, blank=True)
    audio = models.FileField(null=True, blank=True, verbose_name=_("Audiodatei"))
    phonetic_spelling = models.TextField(null=True, blank=True, verbose_name=_("Lautschrift"))
    language = models.CharField(max_length=200, verbose_name=_("Sprache"), null=True, blank=False,
                                choices=language_choices)
