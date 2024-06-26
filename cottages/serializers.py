from decimal import Decimal

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


class CottageInfoWithRatingSerializer(serializers.ModelSerializer):
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
        data['average_rating'] = round(float(data['average_rating']), 1)
        data['price'] = int(instance.price)
        return data


class CottageCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cottage
        fields = [
            'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "guests", "beds", "total_area", "rooms", "parking_places", "check_in_time",
            "check_out_time", "rules", "amenities",
        ]

    def create(self, validated_data):
        if 'price' in validated_data:
            validated_data['price'] = Decimal(validated_data['price'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'price' in validated_data:
            validated_data['price'] = Decimal(validated_data['price'])
        return super().update(instance, validated_data)


class TimeWithoutSecondsField(serializers.TimeField):
    def to_representation(self, value):
        if value:
            formatted_time = value.strftime('%H:%M')
            return formatted_time
        return None


class CottageDetailSerializer(CottageCreateUpdateSerializer):
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
    price = serializers.SerializerMethodField()

    class Meta:
        model = Cottage
        fields = [
            'id', 'town', 'category', "name", "description", 'address', "latitude", "longitude", "price",
            "owner", "guests", "beds", "total_area", "rooms", "images", "parking_places", "check_in_time",
            "check_out_time", "rules", "amenities", "average_rating", "average_location_rating",
            "average_cleanliness_rating", "average_communication_rating", "average_value_rating", "occupied_dates"
        ]

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        return self.round_ratings(data)

    # noinspection PyMethodMayBeStatic
    def round_ratings(self, data: dict) -> dict:
        """Make decimal ratings to float"""
        data['average_rating'] = round(float(data['average_rating']), 1)
        data['average_location_rating'] = round(float(data['average_location_rating']), 1)
        data['average_cleanliness_rating'] = round(float(data['average_cleanliness_rating']), 1)
        data['average_communication_rating'] = round(float(data['average_communication_rating']), 1)
        data['average_value_rating'] = round(float(data['average_value_rating']), 1)
        return data

    @staticmethod
    def get_occupied_dates(obj: Cottage) -> dict:
        """Return occupied days of cottage"""
        all_dates = UserCottageRent.objects.filter(cottage=obj.pk).values_list('start_date', 'end_date')
        closed_days = []
        start_days = []
        for start_date, end_date in all_dates:
            start_days.append(start_date)
            current_date = start_date + relativedelta(days=1)
            while current_date < end_date:
                closed_days.append(current_date)
                current_date += relativedelta(days=1)
        return {"closed_days": closed_days, "start_days": start_days}

    @staticmethod
    def get_price(obj: Cottage):
        return int(obj.price)


class ImageUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    image = serializers.CharField(read_only=True)
    order = serializers.IntegerField()

    class Meta:
        model = CottageImage
        fields = ['id', 'image', 'order']

    @staticmethod
    def validate_order(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Order должен быть целым числом.")
        return value
