from rest_framework import serializers
from reviews.models import Categories


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories
