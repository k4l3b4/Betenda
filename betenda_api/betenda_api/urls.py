from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('Users.urls')),
    path('api/contributions/', include('Contributions.urls')),
    path('api/posts/', include('Posts.urls')),
    path('api/comments/', include('Comments.urls')),
    path('api/articles/', include('Articles.urls')),
    path('api/hashtags/', include('Users.urls')),
    path('api/reactions/', include('Users.urls')),
    path('api/tags/', include('Users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)