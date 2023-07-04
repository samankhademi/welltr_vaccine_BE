from django.urls import path
from . import views

urlpatterns = [
    path('', views.labs, name="labs"),
    path('500', views.error500, name="500"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('list', views.order_list, name="order_list"),
    path('qr-code', views.scan_qr, name="scan_qr"),
    path('detail/<int:id>', views.order_detail, name="order_detail"),
    path('order-edit/<int:id>', views.order_edit, name="order_edit"),
    path('transaction', views.exchange_transaction, name="exchange_transaction"),
    path('search', views.order_search, name="order_search"),
    path('update', views.payment_update, name="payment_update"),
]
