"""URL configuration for the account app."""

from django.urls import path
from .views import (
    RegisterUserView,
    RegisterActiveCode,
    LoginUserGeneric,
    RememberPasswordGeneric,
    ChangePasswordGeneric,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('active_code/', RegisterActiveCode.as_view()),
    path('login/', LoginUserGeneric.as_view()),
    path('remmber_password/', RememberPasswordGeneric.as_view()),
    path('change_password/', ChangePasswordGeneric.as_view()),
]
