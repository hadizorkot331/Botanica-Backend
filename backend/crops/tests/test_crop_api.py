from .test_setup import TestModelSetup
from rest_framework import status
from django.urls import reverse


class TestCropAPI(TestModelSetup):
    def test_crop_add(self):
        crop_list_create_url = reverse("user-plants-list")
        response = self.client.post(
            crop_list_create_url,
            {"crop_id": 1, "lat": 35, "lon": 35, "prediction_probability": 100},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_crop_add_then_list(self):
        # Add dummy crop
        crop_list_create_url = reverse("user-plants-list")
        self.client.post(
            crop_list_create_url,
            {"crop_id": 1, "lat": 35, "lon": 35, "prediction_probability": 100},
        )

        response = self.client.get(crop_list_create_url)
        jsonData = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure that correct number of plants were added
        self.assertEqual(len(jsonData), 1)

    def test_crop_create_then_update(self):
        # Add dummy crop
        crop_list_create_url = reverse("user-plants-list")
        self.client.post(
            crop_list_create_url,
            {"crop_id": 1, "lat": 35, "lon": 35, "prediction_probability": 100},
        )

        # Patch request with no modifications to simulate plant watering
        crop_update_url = reverse("user-plants-update", kwargs={"pk": 1})
        response = self.client.patch(crop_update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crop_create_then_delete(self):
        # Add dummy crop
        crop_list_create_url = reverse("user-plants-list")
        self.client.post(
            crop_list_create_url,
            {"crop_id": 1, "lat": 35, "lon": 35, "prediction_probability": 100},
        )

        crop_delete_url = reverse("user-plants-delete", kwargs={"pk": 1})
        response = self.client.delete(crop_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
