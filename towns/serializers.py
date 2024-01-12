from rest_framework import serializers

from towns.models import Town, TownAttraction, TownImage


class TownImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TownImage
        fields = ['image']


class TownNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Town
        fields = ["id", "name"]


class TownAttractionNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TownAttraction
        fields = ["id", "name"]


class TownSerializer(serializers.ModelSerializer):
    images = TownImageSerializer(many=True, read_only=True)
    attractions = TownAttractionNameSerializer(many=True, read_only=True)

    class Meta:
        model = Town
        fields = ["id", "name", "description", "images", "attractions"]


class TownAttractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TownAttraction
        fields = ["id", "name", "description"]
