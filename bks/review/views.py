from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .serializers import ReviewSerializer
from ..map.models import Facility
from ..map.serializers import FacilitySerializer


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


class ReviewAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request,facilityPk):
        facility =get_object_or_404(Facility, pk=facilityPk)
        review = Facility.objects.filter(facility=facility)
        facility_serializer = FacilitySerializer(facility)
        review_serializer = ReviewSerializer(review, many=True)
        return Response({'facility': facility_serializer.data, 'review': review_serializer.data})
    def post(self, request, facilityPk):
        facility = get_object_or_404(Facility, pk=facilityPk)
        review_form = ReviewForm(request.data)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.facility = facility
            review.created_by = request.user
            review.save()

            response_data = {
                "message": "팀이 생성되었습니다.",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            errors.update(review_form.errors)
            return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)