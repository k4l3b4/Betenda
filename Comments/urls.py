from django.urls import path, re_path
from .views import Comment_CUD_View, Comment_List_View


urlpatterns = [
    path('comment', Comment_CUD_View.as_view({'post':'comment'}),
         name="comment_view"),
    path('reply', Comment_CUD_View.as_view({'post':'reply'}),
         name="comment_view"),
    path('update', Comment_CUD_View.as_view({'post':'update'}),
         name="comment_view"),
    path('delete', Comment_CUD_View.as_view({'post':'delete'}),
         name="comment_view"),
    path('list', Comment_List_View.as_view(),
         name="comment_list_view"),
]
