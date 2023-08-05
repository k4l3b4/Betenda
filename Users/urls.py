from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthorSearchView, CurrentUserView, FollowerRequestListView, LoginView, User_GET_View, UserCreateView, UserProfileFollowAPIView


urlpatterns = [

    path('current_user', CurrentUserView.as_view(
        {'get': 'get_current_user'}), name="current_user_view"),
        
    path('filtered_users', CurrentUserView.as_view(
        {'get': 'get_filtered_users'}), name="filtered_users_view"),

    path('top_accounts', CurrentUserView.as_view(
        {'get': 'get_top_accounts'}), name="top_accounts_view"),

    path('mutual_users', CurrentUserView.as_view(
        {'get': 'mutual_friends_following'}), name="mutual_friends_view"),

    path('profile', CurrentUserView.as_view(
        {'patch': 'update_current_user'}), name="update_current_user_view"),
    path('get_user', CurrentUserView.as_view(
        {'get': 'get_user'}), name="get_user_view"),
    path('login', LoginView.as_view(), name="login_view"),
    path('register/<str:code>', UserCreateView.as_view(),
         name="create_account_view"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),

    path('search_author', AuthorSearchView.as_view(), name='search_author_view'),

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
