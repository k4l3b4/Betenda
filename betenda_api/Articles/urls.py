from django.urls import path
from .views import Article_CUD_View


urlpatterns = [
    path('article', Article_CUD_View.as_view(), name="article_create_update_delete_view")
]
