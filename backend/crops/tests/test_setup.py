from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from ..models import Crop


class TestModelSetup(APITestCase):
    """
    When running tests, django creates a new testing database completely separate from the original database.
    There are ways to copy data like fixtures, but that exposes the entire database data for a certain model, which is not great.
    Instead, in the setup, we create a temporary crop we use for testing

    Note: setUp runs once before every METHOD, meaning the db transaction is rolled back after the method concludes.
    In order to persist data across test methods, we use setUpTestData, which runs once before the TEST CLASS

    Note: setUpSelfData is a classmethod, which takes the class cls, instead of self which is an instance of the class.
    It also only has access to class level methods and data
    """

    @classmethod
    def setUpTestData(cls):
        # Add dummy crop to test db
        Crop.objects.create(
            name="Maize",
            crop_yield=1.2,
            indoor=False,
            cycle="annual",
            watering="medium",
            watering_avg_volume_requirement=40,
            pruning_month="none",
            growth_rate="high",
            min_hardiness=-2,
            max_hardiness=35,
            image_url="https://pngimg.com/d/corn_PNG5284.png",
            sunlight="full_sun",
            days_to_yield=100,
        )

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testUser", password="testPassword")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(self.refresh.access_token)}"
        )
