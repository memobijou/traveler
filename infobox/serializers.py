from rest_framework import serializers
from infobox.models import Category, Infobox


class InfoboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infobox
        fields = ('id', 'title', "description", 'category',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'parent', "child_categories", "infoboxes",)
        #  need to deploy !!
