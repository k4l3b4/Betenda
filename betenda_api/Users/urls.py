from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserCreateView


urlpatterns = [
    path('register/<str:code>', UserCreateView.as_view(), name="create_account_view"),
    path('login', LoginView.as_view(), name="login_view"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
]
