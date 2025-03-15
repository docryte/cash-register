from django.test import TestCase
from decimal import Decimal
from store.models import Item


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(title="Test Item", price=Decimal("10.99"))

    def test_item_creation(self):
        """Тест создания объекта Item"""
        self.assertEqual(self.item.title, "Test Item")
        self.assertEqual(self.item.price, Decimal("10.99"))

    def test_formatted_price(self):
        """Тест форматирования цены"""
        self.assertEqual(self.item.formatted_price, "10.99")

    def test_str_representation(self):
        """Тест строкового представления объекта"""
        expected_str = f"({self.item.id}) Test Item - 10.99"
        self.assertEqual(str(self.item), expected_str)

    def test_price_decimal_places(self):
        """Тест правильности хранения десятичных знаков цены"""
        item = Item.objects.create(title="Decimal Test", price=Decimal("10.999"))
        self.assertEqual(item.price, Decimal("11.00"))

    def test_title_max_length(self):
        """Тест максимальной длины названия"""
        max_length = Item._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)
