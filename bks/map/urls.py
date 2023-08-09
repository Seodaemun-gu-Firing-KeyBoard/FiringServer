from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test", views.test, name="test"),
    path("facilityInfo", views.FacilityInfoAPIView.as_view(), name="facilityInfo"),
]