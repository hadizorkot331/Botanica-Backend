from django.test import TestCase
from ..services.crop_predictor import CropPredictor


class TestCropPredictorAPIs(TestCase):
    def setUp(self):
        self.cp = CropPredictor()

    # Note: Tests will fail if something inside them throws an exception
    # So, just calling the method inside the test is enough

    def test_get_soil_data(self):
        self.cp.get_soil_data(33.716222, 36.198984)

    def test_get_weather_data(self):
        self.cp.get_weather_data(33.716222, 36.198984)
