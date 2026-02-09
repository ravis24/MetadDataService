from rest_framework import serializers
from .models import Dataset, DataElement


class DataElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataElement
        fields = "__all__"
        read_only_fields = ("dataset",)


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"


class DatasetDetailSerializer(serializers.ModelSerializer):
    elements = DataElementSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ["id", "name", "description", "elements"]
