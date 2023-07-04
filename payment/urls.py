from django.urls import path

from . import views

urlpatterns = [
    path("get-link/", views.GetPaymentLinkView.as_view(), name="get-link"),
    path("callback/<str:payment_type>/<str:transaction_uid>/", views.CallbackView.as_view(), name="callback"),
    path("exchange/", views.PaymentByExchangeView.as_view(), name="exchange"),
    path("usdt-transaction/", views.PaymentByUsdtView.as_view(), name="usdt_transaction"),
    path("usdt-transaction/create/", views.CreateUsdtTransaction.as_view(), name="create_usdt_payment"),
    path("usdt-transaction/update/<str:order_id>/", views.UpdateUsdtTransaction.as_view(), name="update_usdt_payment"),
]
