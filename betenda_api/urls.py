from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('Users.urls')),
    path('api/contributions/', include('Contributions.urls')),
    path('api/posts/', include('Posts.urls')),
    path('api/comments/', include('Comments.urls')),
    path('api/articles/', include('Articles.urls')),
    path('api/hashtags/', include('Users.urls')),
    path('api/reactions/', include('Reactions.urls')),
    path('api/notifications/', include('Notifications.urls')),
    path('api/roadmap/', include('RoadMaps.urls')),
    path('api/donations/', include('Donations.urls')),
    path('api/donations/', include('Donations.urls')),
    path('api/bookmark/', include('BookMarks.urls')),
    path("debug/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
