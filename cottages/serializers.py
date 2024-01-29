from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from cottages.models import Cottage, CottageCategory, CottageImage
from relations.models import UserCottageRent
from towns.serializers import TownNameSerializer
from users.serializers import UserFullNameSerializer


class CottageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageImage
        fields = ['id', 'image', 'order']


class CottageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageCategory
        fields = ["id", "name"]


class CottageListSerializer(serializers.ModelSerializer):
    images = CottageImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)

    class Meta:
        model = Cottage
        fields = ['id', 'town', 'category', "name", "price", "guests", "total_area",
                  "beds", "rooms", "average_rating", "images"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Round the float to one decimal place
        data['average_rating'] = round(float(data['average_rating']), 1)
        return data


class CottageCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    images = CottageImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "guests", "beds", "total_area", "rooms", "images", "parking_places", "check_in_time",
            "check_out_time", "rules", "amenities",
        ]


class TimeWithoutSecondsField(serializers.TimeField):
    def to_representation(self, value):
        if value:
            formatted_time = value.strftime('%H:%M')
            return formatted_time
        return None


class CottageDetailUpdateSerializer(CottageCreateSerializer):
    owner = UserFullNameSerializer(read_only=True)
    town = TownNameSerializer(read_only=True)
    category = CottageCategorySerializer(read_only=True)
    check_in_time = TimeWithoutSecondsField()
    check_out_time = TimeWithoutSecondsField()
    average_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    average_location_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    average_cleanliness_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    average_communication_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    average_value_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    occupied_dates = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "owner", "guests", "beds", "total_area", "rooms", "images", "parking_places", "check_in_time",
            "check_out_time", "rules", "amenities", "average_rating", "average_location_rating",
            "average_cleanliness_rating", "average_communication_rating", "average_value_rating", "occupied_dates"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Round the float to one decimal place
        data['average_rating'] = round(float(data['average_rating']), 1)
        data['average_location_rating'] = round(float(data['average_location_rating']), 1)
        data['average_cleanliness_rating'] = round(float(data['average_cleanliness_rating']), 1)
        data['average_communication_rating'] = round(float(data['average_communication_rating']), 1)
        data['average_value_rating'] = round(float(data['average_value_rating']), 1)
        return data

    def get_occupied_dates(self, obj):
        all_dates = UserCottageRent.objects.filter(cottage=obj.pk).values_list('start_date', 'end_date')
        all_dates_list = []
        for start_date, end_date in all_dates:
            current_date = start_date
            while current_date <= end_date:
                all_dates_list.append(current_date)
                current_date += relativedelta(days=1)
        return all_dates_list


class ImageUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    image = serializers.CharField(read_only=True)
    order = serializers.IntegerField()

    class Meta:
        model = CottageImage
        fields = ['id', 'image', 'order']

    def validate_order(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Order должен быть целым числом.")
        return value
