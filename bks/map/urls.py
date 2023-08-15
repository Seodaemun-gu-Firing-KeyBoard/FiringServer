from django.urls import path
from . import views

#서버주소/map/ 붙이고 아래 링크들이 들어가는 것!
urlpatterns = [
    #지도 보기
    path("", views.map, name="map"),
    #크롤링 하기(데이터는 db에서 확인 가능)
    path("crawl/", views.CrawlAPIView.as_view(), name="crawl"),
    #시설 목록 보기
    path("facility/", views.FacilityAPIView.as_view(), name="facility"),
    #시설별로 확인
    path("facility/<int:id>/", views.FacilityDetailAPIView.as_view(), name="facility_detail"),
    path("facilityType/", views.FacilityTypeAPIView.as_view(), name="facilityType"),
    path("facilityDetailType/", views.FacilityDetailTypeAPIView.as_view(), name="facilityDetailType"),
    path("facilityFee/", views.FacilityFeeAPIView.as_view(), name="facilityFee"),
]