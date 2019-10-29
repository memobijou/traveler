from rest_framework import serializers
from infobox.models import Category, Infobox


class ChildInfoboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infobox
        fields = ('id', 'title', "parent", "description", 'category', "language", "type", "audio", )


class InfoboxSerializer(serializers.ModelSerializer):
    infobox_set = ChildInfoboxSerializer(many=True)

    class Meta:
        model = Infobox
        fields = ('id', 'title', "description", "parent", 'category', "language", "type", "audio", "infobox_set",)


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
