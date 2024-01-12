import datetime

from rest_framework.test import APITestCase

from cottages.models import Cottage, CottageAmenities, CottageCategory, CottageRules
from relations.models import UserCottageReview
from towns.models import Town, TownAttraction
from users.models import User


class APITestCaseWithSetUp(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test@example.com',
            password='Test123',
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            is_staff=True
        )
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            password='Test123',
            phone_number='0123456789',
            first_name='John',
            last_name='Doe'
        )
        self.category1 = CottageCategory.objects.create(
            name="cottage",
        )
        self.town1 = Town.objects.create(
            name="Vladikavkaz",
            description="Город есть на Тереке один"
        )
        self.attraction1 = TownAttraction.objects.create(
            name="Batman",
            town=self.town1,
            description="123132"
        )
        self.cottage1 = Cottage.objects.create(
            user=self.user1,
            town=self.town1,
            category=self.category1,
            name="Family",
            description="Very good cottage",
            address='Test Address',
            latitude=40.7128,
            longitude=-74.0060,
            price=9500,
            guests=5,
            beds=4,
            rooms=3,
            total_area=50,
        )
        self.rules1 = CottageRules.objects.create(
            cottage=self.cottage1,
            check_in_time=datetime.time(hour=12),
            check_out_time=datetime.time(hour=12),
            with_children=True,
            with_pets=False,
            smoking=False,
            parties=True,
            need_documents=True
        )
        self.amenities1 = CottageAmenities.objects.create(
            cottage=self.cottage1,
            parking_spaces=2,
            wifi=True,
            tv=False,
            air_conditioner=True,
            hair_dryer=False,
            electric_kettle=True
        )
        self.review1 = UserCottageReview.objects.create(
            cottage=self.cottage1,
            user=self.user1,
            cottage_rating=4,
            cleanliness_rating=3,
            owner_rating=5,
            comment="Все отлично",
        )
