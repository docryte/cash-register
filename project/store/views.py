import logging
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from .models import Item
from .services.pdf_service import WkhtmltopdfConverter
from .services.qr_service import QRGenerator
from .services.receipt_service import ReceiptContextBuilder, ReceiptService
from .services.html_service import DjangoHTMLRenderer
from .serializers import (
    ItemSerializer,
    ReceiptRequestSerializer,
)
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """
    Пагинация для результатов запросов.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ItemViewSet(viewsets.ModelViewSet):
    """
    API для работы с товарами.
    Позволяет просматривать и управлять товарами.
    """

    queryset = Item.objects.all().order_by("id")
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]


class CashMachineViewSet(APIView):
    """
    API для работы с кассовым аппаратом.
    Позволяет создавать чеки с QR-кодами.
    """

    throttle_classes = [UserRateThrottle]

    _receipt_service = ReceiptService(
        pdf_service=WkhtmltopdfConverter(),
        html_service=DjangoHTMLRenderer(),
        context_builder=ReceiptContextBuilder(),
    )
    _qr_service = QRGenerator()

    @swagger_auto_schema(
        operation_description="Создание чека",
        request_body=ReceiptRequestSerializer,
        responses={200: "OK", 400: "Bad Request"},
    )
    def post(self, request):
        """
        Создает чек на основе списка товаров. Возвращает QR-код.
        """
        serializer = ReceiptRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_ids = serializer.validated_data["items"]
        items = Item.objects.filter(id__in=item_ids)

        if not items.exists():
            return Response(
                {"error": "Нет товаров по переданным ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            receipt_data = self._receipt_service.create_receipt(items)
            uri = request.build_absolute_uri(receipt_data.relative_pdf_uri)
            qr_buffer = self._qr_service.generate(uri)

            return FileResponse(
                qr_buffer,
                status=status.HTTP_200_OK,
                content_type="image/png",
                as_attachment=False,
                filename="qr.png",
            )

        except ValueError as e:
            logger.error(f"Ошибка валидации при создании чека: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except OSError as e:
            logger.error(f"Ошибка файловой системы при создании чека: {str(e)}")
            return Response(
                {"error": "Ошибка при создании файлов чека"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании чека: {str(e)}")
            return Response(
                {"error": "Внутренняя ошибка сервера"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
