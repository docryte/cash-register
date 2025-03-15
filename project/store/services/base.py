from abc import ABC, abstractmethod
from typing import Any, Dict, List
from io import BytesIO


class PDFServiceInterface(ABC):
    """
    Интерфейс для сервиса генерации PDF
    """

    @abstractmethod
    def convert_html_to_pdf(self, html: str) -> bytes:
        """
        Конвертирует HTML-строку в PDF файл.
        """
        pass


class HTMLServiceInterface(ABC):
    """
    Интерфейс для сервиса рендеринга HTML
    """

    @abstractmethod
    def render_to_string(self, html_template: str, context: dict) -> str:
        """
        Преобразовывает шаблон с контекстом (переменными для шаблона) в строку HTML
        """
        pass


class QRServiceInterface(ABC):
    """
    Интерфейс для сервиса генерации QR-кодов.
    """

    @abstractmethod
    def generate(self, data: str) -> BytesIO:
        """
        Преобразовывает входную строку в файлоподобный объект с изображением.

        Args:
            data: Данные для кодирования в QR-код

        Returns:
            BytesIO: Буфер с PNG изображением QR-кода

        Note:
            Вызывающий код отвечает за закрытие возвращаемого буфера
        """
        pass


class ReceiptContextBuilderInterface(ABC):
    """Интерфейс для построителя контекста чека."""

    @abstractmethod
    def build_context(self, items: List[Any], total: float) -> Dict[str, Any]:
        """Создает контекст для шаблона чека."""
        pass


class ReceiptServiceInterface(ABC):
    """Интерфейс для сервиса работы с чеками."""

    @abstractmethod
    def create_receipt(self, items: List[Any]) -> Any:
        """Создает чек на основе списка товаров."""
        pass
