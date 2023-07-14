from django.urls import path
from Posts.views import Post_CUD_View, Post_List_View


urlpatterns = [
    path('get_posts', Post_List_View.as_view(), name="post_list_view"),
    path('post', Post_CUD_View.as_view(), name="post_create_update_delete_view"),
]