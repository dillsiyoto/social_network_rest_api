from django.urls import path
from users.views import (
    RegistrationApiView,
    UserListApiView,
    UserDetailsApiView,
    ChangePasswordApiView,
)

urlpatterns = [
    path("register/", RegistrationApiView.as_view(), name="user-register"),
    path("users/", UserListApiView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailsApiView.as_view(), name="user-details"),
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password"),
]