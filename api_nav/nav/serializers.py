from rest_framework import serializers
from .models import NestedCategory


class CategorySerializer(serializers.Serializer):
    # category_id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    lft = serializers.IntegerField()
    rgt = serializers.IntegerField()

    def create(self, validated_data):
        return NestedCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.lft = validated_data.get('lft', instance.lft)
        instance.rgt = validated_data.get('rgt', instance.rgt)
        instance.save()
        return instance
