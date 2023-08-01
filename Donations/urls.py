from django.urls import path
from .views import Campaign_CU_View

urlpatterns = [
    path('campaign', Campaign_CU_View.as_view(), name="campaign_create_update_view")
]
