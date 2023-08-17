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
    #시설종류별로 확인
    path("facilityType/", views.FacilityTypeAPIView.as_view(), name="facilityType"),
    #시설세부종류별로 확인
    path("facilityDetailType/", views.FacilityDetailTypeAPIView.as_view(), name="facilityDetailType"),
    #요금 필터링
    path("facilityFee/", views.FacilityFeeAPIView.as_view(), name="facilityFee"),
    #위치 필터링
    path("facilityAddress/", views.FacilityAddressAPIView.as_view(), name="facilityAddress"),
]