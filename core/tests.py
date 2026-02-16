from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Dataset, DataElement

class DatasetModelTest(TestCase):

    def test_create_dataset(self):
        dataset = Dataset.objects.create(
            name="Customer",
            description="Customer dataset"
        )
        self.assertEqual(dataset.name, "Customer")
        self.assertEqual(Dataset.objects.count(), 1)


class DataElementModelTest(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Customer",
            description="Customer dataset"
        )

    def test_create_data_element(self):
        element = DataElement.objects.create(
            dataset=self.dataset,
            name="email",
            data_type="string",
            is_required=True
        )
        self.assertEqual(element.name, "email")
        self.assertEqual(DataElement.objects.count(), 1)

    def test_unique_constraint(self):
        DataElement.objects.create(
            dataset=self.dataset,
            name="email",
            data_type="string"
        )

        with self.assertRaises(Exception):
            DataElement.objects.create(
                dataset=self.dataset,
                name="email",
                data_type="string"
            )


class DatasetAPITest(APITestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Customer",
            description="Customer dataset"
        )

    def test_list_datasets(self):
        response = self.client.get("/api/datasets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dataset(self):
        data = {
            "name": "Order",
            "description": "Order dataset"
        }
        response = self.client.post("/api/datasets/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_dataset_detail(self):
        response = self.client.get(f"/api/datasets/{self.dataset.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dataset(self):
        data = {
            "name": "Updated",
            "description": "Updated description"
        }
        response = self.client.put(
            f"/api/datasets/{self.dataset.id}/",
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dataset(self):
        response = self.client.delete(
            f"/api/datasets/{self.dataset.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class DataElementAPITest(APITestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="Customer",
            description="Customer dataset"
        )

    def test_create_data_element(self):
        data = {
            "name": "email",
            "data_type": "string",
            "is_required": True
        }

        response = self.client.post(
            f"/api/datasets/{self.dataset.id}/elements/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_data_elements(self):
        DataElement.objects.create(
            dataset=self.dataset,
            name="email",
            data_type="string"
        )

        response = self.client.get(
            f"/api/datasets/{self.dataset.id}/elements/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


