from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny

from .models import Review
from .models import Facility
from .serializers import ReviewSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.data.get('facility_id')
        facility = Facility.objects.get(id=facility_id)
        serializer.save(user=user, facility=facility)

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        user = self.request.user
        facility_id = self.request.data.get('facility_id')
        facility = Facility.objects.get(id=facility_id)
        serializer.save(user=user, facility=facility)
