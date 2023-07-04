from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("otp/", views.OTPView.as_view(), name="otp"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("upload/<str:uuid>/", views.upload_view, name="upload"),
    path("persons/", views.AddPersonView.as_view(), name="add_person"),
    path("persons/edit", views.EditPersonView.as_view(), name="edit_person"),
    path("persons/edit/bulk/", views.EditPersonBulkView.as_view(), name="edit_person_bulk"),
    path("persons/delete", views.DeletePersonView.as_view(), name="delete_person"),
]
