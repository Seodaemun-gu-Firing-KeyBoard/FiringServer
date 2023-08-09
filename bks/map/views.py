from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .serializers import *
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def home(request):
    return render(request, 'map/home.html')
def test(request):
    return render(request, 'map/test.html')

class FacilityInfoAPIView(APIView):
    def get(self, request):
        facility = Facility.objects.all()
        facility_serializer = FacilitySerializer(facility, many=True)
        return Response({'facility':facility_serializer.data})
    def post(self, request):
        facility_form = FacilityForm(request.data)

        if facility_form.is_valid():
            facility = facility_form.save(commit=False)
            facility.save()
            
            return Response({'message': '시설 추가 완료'}, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            errors.update(facility_form.errors)
            return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)
