from django.urls import path
from RoadMaps.views import GaolListView, Goal_CUD_View, Goal_STATE_View


urlpatterns = [
    path('goal', Goal_CUD_View.as_view(),
         name="goals_create_update_delete_view"),
    path('goals', GaolListView.as_view(), name="goals_list_views"),

    path('achieved/<int:pk>', Goal_STATE_View.as_view({'post': 'achieved'}), name="achieve_goal_views"),
    path('cancel/<int:pk>', Goal_STATE_View.as_view({'post': 'cancel'}), name="cancel_goal_views"),
]
