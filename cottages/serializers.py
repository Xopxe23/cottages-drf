from rest_framework import serializers

from cottages.models import Cottage
from users.serializers import UserSerializer


class CottageSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Cottage
        fields = ['id', 'owner', 'address', 'latitude', 'longitude', 'options']
