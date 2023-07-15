from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserCreateView, UserProfileFollowAPIView


urlpatterns = [
    path('register/<str:code>', UserCreateView.as_view(),
         name="create_account_view"),
    path('login', LoginView.as_view(), name="login_view"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    
    path('follow/<int:pk>', UserProfileFollowAPIView.as_view(), {'post': 'follow'}, name='follow_user_view'),
    path('unfollow/<int:pk>',
         UserProfileFollowAPIView.as_view(), {'post': 'unfollow'}, name='unfollow_user_view'),
]
