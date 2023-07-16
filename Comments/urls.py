from django.urls import path, re_path
from .views import Comment_CUD_View, Comment_List_View


urlpatterns = [
    path('comment', Comment_CUD_View.as_view(),
         name="comment_create_update_delete_view"),
    path('list', Comment_List_View.as_view(),
         name="comment_list_view"),
]
