from django.urls import path
from Posts.views import Post_CUD_View, Post_List_GET_View


urlpatterns = [
    path('get_posts', Post_List_GET_View.as_view(
        {'get': 'list'}), name="post_list_view"),

    path('posts_by_tag', Post_List_GET_View.as_view(
        {'get': 'get_post_with_tag'}), name="post_filter_with_tag_view"),
    path('get_post/<slug:slug>', Post_List_GET_View.as_view(
        {'get': 'get_post'}), name="get_replies_by_slug"),
    path('get_replies', Post_List_GET_View.as_view(
        {'get': 'get_post_replies'}), name="get_replies_by_parent_id"),
    path('post', Post_CUD_View.as_view(),
         name="post_create_update_delete_view"),
]
