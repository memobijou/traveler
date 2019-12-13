from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from supplication.models import Supplication
from supplication.serializers import SupplicationSerializer, SupplicationVariantSerializer


class SupplicationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SupplicationSerializer
    queryset = Supplication.objects.all()
