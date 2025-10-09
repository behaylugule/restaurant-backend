# restaurantrag/urls.py
from django.urls import path
from .views import RAGIngestView

urlpatterns = [
    path("upload/<int:restaurant_id>/", RAGIngestView.as_view(), name="rag-upload"),
]
