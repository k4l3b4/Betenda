from django.urls import path
from .views import Article_CUD_View, Article_Get_View, Article_List_View, Article_Search_View, Article_Trending_View


urlpatterns = [
    path('article', Article_CUD_View.as_view(), name="article_create_update_delete_view"),
    path('search', Article_Search_View.as_view(), name="article_search_view"),
    path('list', Article_List_View.as_view(), name="article_list_view"),
    path('trending', Article_Trending_View.as_view(), name="trending_article_view"),
    path('<slug:slug>', Article_Get_View.as_view(), name="article_get_view")
]
