# restaurantrag/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import update_restaurant_embeddings_task

class RAGIngestView(APIView):
    """
    Asynchronously trigger restaurant embedding generation with Celery.
    """

    def post(self, request, restaurant_id):
        try:
            task = update_restaurant_embeddings_task.delay(restaurant_id)
            return Response(
                {
                    "message": f"Embedding job queued for restaurant {restaurant_id}",
                    "task_id": task.id,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
