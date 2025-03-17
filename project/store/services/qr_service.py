from io import BytesIO
import qrcode
from .base import QRServiceInterface


class QRGenerator(QRServiceInterface):
    """
    Сервис для генерации QR-кодов.
    """

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
