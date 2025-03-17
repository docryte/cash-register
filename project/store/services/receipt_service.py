from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4
from django.conf import settings
from .base import (
    ReceiptServiceInterface,
    ReceiptContextBuilderInterface,
    PDFServiceInterface,
    HTMLServiceInterface,
)


from typing import NamedTuple


class ReceiptData(NamedTuple):
    """
    Данные чека.
    """

    receipt_id: str
    receipt_date: str
    total_sum: float
    relative_pdf_uri: str

    def __str__(self):
        """
        Возвращает строковое представление чека.
        """
        return f"Чек №{self.receipt_id} от {self.receipt_date} \
            на сумму {self.total_sum}\n \
            Хранится по адресу: {self.relative_pdf_uri}"


class ReceiptContextBuilder(ReceiptContextBuilderInterface):
    """
    Построитель контекста для чека.
    """

    def build_context(self, items: List[Any], total: float) -> Dict[str, Any]:
        """
        Создает контекст для шаблона чека.

        Args:
            items: Список товаров
            total: Общая сумма

        Returns:
            Dict[str, Any]: Контекст для шаблона
        """
        return {
            "items": items,
            "total_sum": total,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "receipt_id": uuid4(),
        }


class ReceiptService(ReceiptServiceInterface):
    """
    Сервис для работы с чеками.
    """

    def __init__(
        self,
        pdf_service: PDFServiceInterface,
        html_service: HTMLServiceInterface,
        context_builder: ReceiptContextBuilderInterface,
    ):
        """
        Инициализация сервиса.

        Args:
            pdf_service: Сервис для генерации PDF
            html_service: Сервис для рендеринга HTML
            context_builder: Построитель контекста
        """
        self.pdf_service = pdf_service
        self.html_service = html_service
        self.context_builder = context_builder

    def _calculate_total(self, items: List[Any]) -> float:
        """
        Рассчитывает общую сумму чека.

        Args:
            items: Список товаров

        Returns:
            float: Общая сумма
        """
        return sum(item.price for item in items)

    def _generate_pdf_path(self, filename: str) -> str:
        """
        Генерирует путь для PDF файла.

        Args:
            receipt_id: ID чека

        Returns:
            str: Путь к PDF файлу
        """
        return f"{settings.MEDIA_ROOT}/{filename}.pdf"

    def create_receipt(self, items: List[Any]) -> ReceiptData:
        """
        Создает чек на основе списка товаров.

        Args:
            items: Список товаров

        Returns:
            Any: Данные созданного чека

        Raises:
            ValueError: Если список товаров пуст
            OSError: Если не удалось создать файлы
        """
        if not items:
            raise ValueError("Список товаров не может быть пустым")

        total = self._calculate_total(items)
        context = self.context_builder.build_context(items, total)

        filename = f"receipt_{context['receipt_id']}"

        pdf_path = self._generate_pdf_path(filename)
        html_content = self.html_service.render_to_string("receipt.html", context)
        self.pdf_service.convert_html_to_pdf(html_content, pdf_path)
        relative_pdf_uri = settings.MEDIA_URL + filename + ".pdf"

        return ReceiptData(
            receipt_id=context["receipt_id"],
            total_sum=total,
            relative_pdf_uri=relative_pdf_uri,
            receipt_date=context["date"],
        )
