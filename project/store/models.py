from django.db import models


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
