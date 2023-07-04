from django.urls import path

from . import views

urlpatterns = [
    path("", views.GetOrderView.as_view(), name="get_order"),
    path("edit/", views.EditOrderView.as_view(), name="edit_order"),
    path("vaccine-center/", views.VaccineCenterView.as_view(), name="get_vaccine_center"),
    path("vaccine-type/", views.VaccineTypeView.as_view(), name="get_vaccine_type"),
    path("complete-order/", views.CompleteOrderView.as_view(), name="complete_order"),
    path("portal/list/", views.ListPortalOrderView.as_view(), name="portal_order_list"),
    path("portal/edit/", views.EditPortalOrderView.as_view(), name="portal_order_edit"),
    path("portal/detail/", views.PortalGetOrderView.as_view(), name="portal_order_edit"),
    path("qrcode/<str:order_id>/", views.generate_labs_qr, name='generate_labs_qr'),
    path("qrcode/general/<str:user_text>/", views.generate_general_qr, name='generate_labs_qr'),
    path("coupons/inquiry/", views.CouponsInquiry.as_view(), name='coupons_inquiry'),
    path("packages/", views.HotelPackageView.as_view(), name='search_package'),
    path("hotel-packages/", views.ExternalHotelPackageView.as_view(), name='search_hotel_package'),
]
