from django.urls import include, path
from rest_framework import routers
from .views import ItemViewSet, CashMachineViewSet

router = routers.DefaultRouter()
router.register(r"items", ItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("cash_machine/", CashMachineViewSet.as_view(), name="cash_machine"),
]
