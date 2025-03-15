import os
import subprocess
from django.conf import settings
from .base import PDFServiceInterface


class WkhtmltopdfConverter(PDFServiceInterface):
    """
    Конвертер HTML в PDF с использованием wkhtmltopdf.
    """
    def __init__(self, wkhtmltopdf_path: str = None):
        self.wkhtmltopdf_path = wkhtmltopdf_path or settings.WKHTMLTOPDF_PATH


    def convert_html_to_pdf(self, html_content: str, output_path: str) -> str:
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
        if not os.path.exists(self.wkhtmltopdf_path):
            raise OSError(f"wkhtmltopdf не найден по пути: {self.wkhtmltopdf_path}")

        temp_html = output_path.replace(".pdf", ".html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        try:
            cmd = [
                self.wkhtmltopdf_path,
                "--encoding",
                "utf-8",
                "--margin-top",
                "0",
                "--margin-bottom",
                "0",
                "--margin-left",
                "0",
                "--margin-right",
                "0",
                temp_html,
                output_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise ValueError(f"Ошибка конвертации: {result.stderr}")

            return output_path

        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)
