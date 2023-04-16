from django.urls import path

from . import views

urlpatterns = [
    path(
        "create-visualization/",
        views.VisualizationsAPIView.as_view(),
        name="visualizations",
    ),
    path("csv/<int:pk>/summary/", views.CSVSummaryView.as_view(), name="summary"),
    path("upload-csv/", views.CSVUploadView.as_view(), name="csv_upload"),
    path("", views.DashboardAPIView.as_view(), name="dashboard"),
]
