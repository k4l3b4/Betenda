from django.urls import path
from Posts.views import Post_CUD_View


urlpatterns = [
    path('post', Post_CUD_View.as_view(), name="post_create_update_delete_view")
]