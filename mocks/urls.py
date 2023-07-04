from django.urls import path

from . import views

urlpatterns = [
    path("<str:host_id>/<str:op_code>/", views.MocksViewset.as_view(), name="mocks"),
]
