from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товаров.
    """
    class Meta:
        model = Item
        fields = ["id", "title", "price"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value


class ReceiptRequestSerializer(serializers.Serializer):
    """
    Сериализатор для запроса на создание чека.
    """
    items = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100,
        help_text="Список ID товаров (от 1 до 100)",
    )
