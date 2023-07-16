from django.urls import path
from .views import Reaction_CREATE_View

urlpatterns = [
    path('react', Reaction_CREATE_View.as_view(), name="reaction_create_delete_view")
]
