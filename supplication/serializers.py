from rest_framework import serializers
from supplication.models import Supplication, SupplicationVariant, SupplicationData


class SupplicationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplicationData
        fields = ("title", "description", "audio", "phonetic_spelling", "language",)


class SupplicationVariantSerializer(serializers.ModelSerializer):
    supplication_data = SupplicationDataSerializer()

    class Meta:
        model = SupplicationVariant
        fields = ('id', 'supplication_data',)


class SupplicationSerializer(serializers.ModelSerializer):
    supplication_data = SupplicationDataSerializer()
    supplicationvariant_set = SupplicationVariantSerializer(many=True)

    class Meta:
        model = Supplication
        fields = ('id', 'type', "supplication_data", 'supplicationvariant_set', )
