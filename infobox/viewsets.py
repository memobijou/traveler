from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from infobox.models import Category, Infobox
from infobox.serializers import CategorySerializer, InfoboxSerializer


class InfoboxViewSet(viewsets.ModelViewSet):
    serializer_class = InfoboxSerializer
    queryset = Infobox.objects.all()

    @action(detail=True)
    def language(self, request, *args, **kwargs):
        language_code = self.request.GET.get("lang")
        instance = self.get_object()

        if language_code == "de":
            language = "Deutsch"
            instance = self.get_infobox_in_language(instance, language)
        elif language_code == "ar":
            language = "Arabisch"
            instance = self.get_infobox_in_language(instance, language)
        elif language_code == "tr":
            language = "Türkisch"
            instance = self.get_infobox_in_language(instance, language)
        elif language_code == "ur":
            language = "Urdu"
            instance = self.get_infobox_in_language(instance, language)
        else:
            instance = None

        if instance is None:
            return Response({"error": "Infobox in der angegeben Sprache nicht vorhanden"})
        serialized_data = InfoboxSerializer(instance=instance)
        return Response(serialized_data.data)

    @staticmethod
    def get_infobox_in_language(instance, language):
        if instance.language == language:
            return instance

        instance = instance.infobox_set.filter(language__icontains=language).first()
        return instance


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
