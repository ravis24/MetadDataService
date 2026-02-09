from django.urls import path
from .views import DatasetAPIView, DatasetDetailAPIView

urlpatterns = [
    path("datasets/", DatasetAPIView.as_view()),
    path("datasets/<int:pk>/", DatasetDetailAPIView.as_view()),
]
