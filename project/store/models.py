from django.db import models
from decimal import Decimal, ROUND_HALF_UP


class Item(models.Model):
    """
    Модель товара.
    """

    class Meta:
        abstract = False

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def formatted_price(self) -> str:
        return f"{self.price:.2f}"

    def __str__(self):
        return f"({self.id}) {self.title} - {self.price}"

    def clean(self):
        """
        Округляет цену до двух знаков после запятой перед сохранением.
        """
        if self.price:
            self.price = Decimal(str(self.price)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        super().clean()

    def save(self, *args, **kwargs):
        """
        Переопределяем метод save для автоматического вызова clean().
        """
        self.clean()
        super().save(*args, **kwargs)
