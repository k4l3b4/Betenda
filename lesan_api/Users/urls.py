from django.urls import path
from .views import LoginView, UserCreateView


urlpatterns = [
    path('register/<str:code>', UserCreateView.as_view(), name="create_account_view"),
    path('login', LoginView.as_view(), name="login_view")
]
