from django.urls import path
from .views import BookMark_LAD_View

urlpatterns = [
    path('list', BookMark_LAD_View.as_view({'get': 'list'}), name="list_bookmark_items_view"),
    path('add', BookMark_LAD_View.as_view({'post': 'add_or_delete'}), name="add_to_bookmark_view"),
]