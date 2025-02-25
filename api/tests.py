from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item

class ItemAPITestCase(APITestCase):
    def setUp(self):
        """
        Runs before each test
        """
        # create an user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # create mock data
        self.item = Item.objects.create(name="Test Item", description="description of item")

        # API urls
        self.list_url = "/api/items/"
        self.detail_url = f"api/items/{self.item.id}/"

        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_get_items(self):
        response = self.client.get(self.list_url) # call the api/items
        self.assertEqual(response.status_code, status.HTTP_200_OK) # asserting the status that should return
        self.assertEqual(len(response.data), 1) # asserting the length

    def test_reate_item(self):
        data = {"name": "mock item", "description": "mock description"}
        response = self.client.post(self.list_url, data, format="json") # json post to api/items
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_get_single_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name']. self.item.name)

    def test_update_item(self):
        updated_data = {"name": " Updated item", "description": "Updated description"}
        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated item")

    def test_delete_item(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
