from rest_framework import viewsets
from infobox.models import Category, Infobox
from infobox.serializers import CategorySerializer, InfoboxSerializer


class InfoboxViewSet(viewsets.ModelViewSet):
    serializer_class = InfoboxSerializer
    queryset = Infobox.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
