from rest_framework import serializers

from towns.models import Town


class TownNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Town
        fields = ["id", "name"]
