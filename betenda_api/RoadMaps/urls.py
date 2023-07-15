from django.urls import path
from RoadMaps.views import GaolListView, Goal_CUD_View


urlpatterns = [
    path('goal', Goal_CUD_View.as_view(), name="goals_create_update_delete_view"),
    path('goals', GaolListView.as_view(), name="goals_list_views")
]
