from django.urls import path
from .views import ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review_list_create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review_retrieve_update_destroy'),
]