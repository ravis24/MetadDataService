from django.urls import path
from .views import DatasetAPIView, DatasetDetailAPIView, DataElementAPIView

urlpatterns = [
    path("datasets/", DatasetAPIView.as_view()),
    path("datasets/<int:pk>/", DatasetDetailAPIView.as_view()),
    path("datasets/<int:dataset_id>/elements/", DataElementAPIView.as_view()),
]
