from django.urls import path
from Reports.views import Reports_List_View, Report_Create_View


urlpatterns = [
    path('report', Report_Create_View.as_view(), name="report_view"),
    path('list', Reports_List_View.as_view(), name="list_reports_view"),
]
