from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Bezeichnung"))
    description = models.TextField(verbose_name=_("Beschreibung"), null=True, blank=True)
    parent = models.ForeignKey("infobox.Category", on_delete=models.SET_NULL, null=True,
                               verbose_name=_("Oberkategorie"), related_name="child_categories")


language_choices = (("Arabisch", "Arabisch"), ("Deutsch", "Deutsch"), ("Türkisch", "Türkisch"), ("Urdu", "Urdu"),)
type_choices = (("Mustahabb", "Mustahabb"), ("Sunnah", "Sunnah"))

class Infobox(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Bezeichnung"))
    language = models.CharField(max_length=200, verbose_name=_("Typ"), null=True, blank=False, choices=language_choices)
    description = models.TextField(verbose_name=_("Beschreibung"), null=True, blank=True)
    category = models.ForeignKey("infobox.Category", verbose_name=_("Kategorie"), on_delete=models.SET_NULL, null=True,
                                 related_name="infoboxes")
    parent = models.ForeignKey("infobox.Infobox", on_delete=models.CASCADE, null=True)
    audio = models.FileField(null=True, blank=True, verbose_name="Audiodatei")
    type = models.CharField(max_length=200, null=True, blank=True, choices=type_choices)
