from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from store.models import Item
from unittest.mock import patch
import io


class ItemViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(title="Test Item", price=Decimal("10.99"))
        self.list_url = reverse("item-list")
        self.detail_url = reverse("item-detail", args=[self.item.id])

    def test_list_items(self):
        """Тест получения списка товаров"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_item(self):
        """Тест создания нового товара"""
        data = {"title": "New Item", "price": "15.99"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_retrieve_item(self):
        """Тест получения конкретного товара"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Item")

    def test_update_item(self):
        """Тест обновления товара"""
        data = {"title": "Updated Item", "price": "20.99"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Updated Item")

    def test_delete_item(self):
        """Тест удаления товара"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)


class CashMachineViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(title="Test Item", price=Decimal("10.99"))
        self.url = reverse("cash_machine")

    @patch("store.views.ReceiptService")
    @patch("store.views.QRGenerator")
    def test_create_receipt_success(self, mock_qr_generator, mock_receipt_service):
        """Тест успешного создания чека"""
        mock_receipt_service.return_value.create_receipt.return_value.relative_pdf_uri = "/test.pdf"
        mock_qr_generator.return_value.generate.return_value = io.BytesIO(
            b"fake-qr-code"
        )

        data = {"items": [self.item.id]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Type"), "image/png")

    def test_create_receipt_invalid_items(self):
        """Тест создания чека с несуществующими товарами"""
        data = {"items": [999]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_receipt_no_items(self):
        """Тест создания чека без товаров"""
        data = {"items": []}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
