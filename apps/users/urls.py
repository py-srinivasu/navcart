from django.urls import path

from apps.users.views import RegistrationView, LoginView

urlpatterns = [
    path('user/', RegistrationView.as_view(), name='user-registration'),
    path('user/login/', LoginView.as_view(), name='user-login'),
]
