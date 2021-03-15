from rest_framework.routers import DefaultRouter
from apps.transaction.views import TransactionViewSet, TransactionTypeViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'transactions-type', TransactionTypeViewSet, basename='transaction-type')

urlpatterns = [
    path('',include(router.urls)),
]