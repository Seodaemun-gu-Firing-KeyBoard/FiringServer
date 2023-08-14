from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test/", views.test, name="test"),
    path("facility/", views.FacilityAPIView.as_view(), name="facility"),
    path("facility_address/", views.FacilityAddressAPIView.as_view(), name="facility_address"),
]