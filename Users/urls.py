from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import FollowerRequestListView, LoginView, User_GET_View, UserCreateView, UserProfileFollowAPIView


urlpatterns = [
    path('login', LoginView.as_view(), name="login_view"),
    path('register/<str:code>', UserCreateView.as_view(),
         name="create_account_view"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),

    path('follow/<int:pk>',
         UserProfileFollowAPIView.as_view({'post': 'follow'}), name='follow_user_view'),
    path('unfollow/<int:pk>',
         UserProfileFollowAPIView.as_view({'post': 'unfollow'}), name='unfollow_user_view'),
    path('requests',
         FollowerRequestListView.as_view(), name='list_follow_requests_view'),
    path('accept/<int:pk>',
         UserProfileFollowAPIView.as_view({'post': 'accept'}), name='accept_follow_view'),
    path('<str:username>', User_GET_View.as_view(), name="user_get_view"),
]
