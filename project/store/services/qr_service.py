from io import BytesIO
from typing import Optional
import qrcode
from .base import QRServiceInterface


class QRGenerator(QRServiceInterface):
    """
    Сервис для генерации QR-кодов.
    """

    def __init__(
        self,
        version: Optional[int] = None,
        error_correction: int = qrcode.constants.ERROR_CORRECT_L,
        box_size: int = 10,
        border: int = 4,
    ):
        """
        Инициализация генератора QR-кодов.

        Args:
            version: Версия QR-кода (1-40)
            error_correction: Уровень коррекции ошибок
            box_size: Размер одного модуля в пикселях
            border: Размер отступа в модулях
        """
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border

    def generate(self, data: str) -> BytesIO:
        """
        Генерирует QR-код из данных.

        Args:
            data: Данные для кодирования

        Returns:
            BytesIO: Буфер с PNG изображением QR-кода

        Raises:
            ValueError: Если данные слишком длинные для выбранной версии
        """
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
