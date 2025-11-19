from django.urls import path

from .views import (
    registration,
    login,
    profile,
    logout,
    change_password,
    forgot_password,
    reset_password,
)

urlpatterns = [
    path("register/", registration.UserRegistrationView.as_view(), name="register"),
    path("login/", login.UserLoginView.as_view(), name="login"),
    path(
        "forgot-password/",
        forgot_password.SendPasswordResetEmailView.as_view(),
        name="forgot-password",
    ),
    path(
        "change-password/",
        change_password.UserChangePasswordView().as_view(),
        name="change-password",
    ),
    path(
        "reset-password/<str:uid>/<str:token>/",
        reset_password.UserPasswordResetView().as_view(),
        name="change-password",
    ),
    path("profile/", profile.UserProfile.as_view(), name="profile"),
    path("logout/", logout.UserLogoutView.as_view(), name="logout"),
]
