from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.ExchangeListApiView.as_view(), name="list"),
    path("portal/search/", views.SearchPortalOrderPayment.as_view(), name="portal_order_search"),
    path("portal/transactions/", views.ListPortalExchangeTransaction.as_view(), name="portal_exchange_transactions"),
]
