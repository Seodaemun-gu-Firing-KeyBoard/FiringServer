from django.urls import path
from .views import ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView, ReviewAPIView

urlpatterns = [
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-retrieve-update-destroy'),

    path('testreview/<int:facilityPK>/', ReviewAPIView.as_view(), name='review')
]