from rest_framework import serializers
from infobox.models import Category, Infobox
from supplication.serializers import SupplicationSerializer


class ChildInfoboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infobox
        fields = ('id', 'title', "parent", "description", 'category', "language", )


class InfoboxSerializer(serializers.ModelSerializer):
    infobox_set = ChildInfoboxSerializer(many=True)
    supplication_set = SupplicationSerializer(many=True)

    class Meta:
        model = Infobox
        fields = ('id', 'title', "description", "parent", 'category', "language", "infobox_set",
                  "supplication_set",)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', "description",)


class CategorySerializer(serializers.ModelSerializer):
    child_categories = SubCategorySerializer(many=True)
    infoboxes = InfoboxSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', "description", 'parent', "child_categories", "infoboxes",)
        #  need to deploy !!!
