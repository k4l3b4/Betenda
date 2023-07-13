"""
URL configuration for lesan_api project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('Users.urls')),
    path('api/contributions/', include('Contributions.urls')),
    path('api/posts/', include('Users.urls')),
    path('api/comments/', include('Users.urls')),
    path('api/articles/', include('Users.urls')),
    path('api/hashtags/', include('Users.urls')),
    path('api/reactions/', include('Users.urls')),
    path('api/tags/', include('Users.urls')),
]
