from django.urls import path
from .views import Article_CUD_View, Article_Get_View, Article_List_View


urlpatterns = [
    path('article', Article_CUD_View.as_view(), name="article_create_update_delete_view"),
    path('list', Article_List_View.as_view(), name="article_list_view"),
    path('get/<slug:slug>', Article_Get_View.as_view(), name="article_get_view")
]
