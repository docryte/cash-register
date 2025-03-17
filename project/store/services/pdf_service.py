from pathlib import Path
from django.conf import settings
from .base import PDFServiceInterface
import pdfkit


class WkhtmltopdfConverter(PDFServiceInterface):
    """
    Конвертер HTML в PDF с использованием wkhtmltopdf.
    """

    def __init__(self, wkhtmltopdf_path: str = None):
        self.wkhtmltopdf_path = wkhtmltopdf_path or settings.WKHTMLTOPDF_PATH

    def convert_html_to_pdf(self, html_content: str, output_file: str) -> str:
        """
        Конвертирует HTML в PDF файл.

        Args:
            html_content: HTML контент для конвертации
            output_path: Путь для сохранения PDF

        Returns:
            str: Путь к созданному PDF файлу

        Raises:
            OSError: Если wkhtmltopdf не установлен или недоступен
            ValueError: Если конвертация не удалась
        """
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        try:
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path or "")
            pdfkit.from_string(html_content, output_file, configuration=config)
        except Exception as err:
            raise ValueError(f"Не удалось сконвертировать HTML в PDF: {err}")

        return output_file
