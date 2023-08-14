from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .serializers import *
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

class FacilityAPIView(APIView):
    def get(self, request):
        code_mapping = {
            100: {
                "name": "체육시설",
                "dCode_mapping": {
                    101: "농구장",
                    # 102: "다목적경기장",
                    # 103: "배구장",
                    # 104: "배드민턴장",
                    # 105: "야구장",
                    # 106: "족구장",
                    # 107: "축구장",
                    # 108: "테니스장",
                    # 109: "풋살장",
                    # 115: "골프장",
                    # 116: "교육시설",
                    # 117: "수영장",
                    # 125: "운동장",
                    # 126: "체육관",
                    # 127: "탁구장"
                }
            },
            200: {
                "name": "문화체험",
                "dCode_mapping": {
                    # 202: "단체봉사",
                    203: "전시/관람",
                    # 204: "문화행사",
                    # 205: "교육체험",
                    # 206: "농장체험",
                    # 207: "공원탐방",
                    # 208: "서울형키즈카페",
                    # 209: "삼림여가"
                }
            },
            500: {
                "name": "공간시설",
                "dCode_mapping": {
                    501: "녹화장소",
                    # 502: "캠핑장",
                    # 504: "강당",
                    # 505: "강의실",
                    # 506: "다목적실",
                    # 507: "전시실",
                    # 508: "주민공유공간",
                    # 509: "회의실",
                    # 510: "민원등기타",
                    # 511: "공연장",
                    # 513: "광장",
                    # 514: "청년공간"
                }
            }
        }

        base_url = "https://yeyak.seoul.go.kr/web/search/selectPageListDetailSearchImg.do?code=T"
        detail_base_url = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id={rsv_svc_id}&code=T{code}&dCode=T{dCode}&sch_order=1&sch_choose_list=&sch_type=&sch_text=&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt=&svc_prior=N&sch_reqst_value="
        results = []

        for code, config in code_mapping.items():
            code_name = config["name"]
            dCode_mapping = config["dCode_mapping"]
            facility_results = []

            for dCode, facility in dCode_mapping.items():
                for page in range(1, 3):  # 페이지 1과 2 가져오기
                    url = base_url + str(code) + "&dCode=T" + str(dCode) + "&currentPage=" + str(page)
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        link_elements = soup.find_all('a', onclick=lambda onclick: onclick and "fnDetailPage" in onclick)
                        for link_element in link_elements:
                            onclick_attr = link_element.get("onclick")
                            rsv_svc_id = onclick_attr.split("'")[1]

                            detail_url = detail_base_url.format(rsv_svc_id=rsv_svc_id, code=code, dCode=dCode)
                            detail_response = requests.get(detail_url, headers={'User-Agent': 'Mozilla/5.0'})

                            if detail_response.status_code == 200:
                                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                                ul_element = detail_soup.find('ul', class_='dt_top_list')
                                if ul_element:
                                    li_elements = ul_element.find_all('li')
                                    data_dict = {}
                                    for li_element in li_elements:
                                        b_element = li_element.find('b', class_='tit1')
                                        if b_element:
                                            label = b_element.text.strip()
                                            content = li_element.get_text(separator="\n", strip=True).replace(label, "").strip()
                                            data_dict[label] = content
                                    address_h5 = detail_soup.find('h5', class_='sub_tit1', text='주소')
                                    if address_h5:
                                        address_p = address_h5.find_next('p', class_='sub_txt1')
                                        if address_p:
                                            address = address_p.text.strip()
                                            data_dict['주소'] = address
                                            facility_instance = Facility(name=facility, address=address)
                                            facility_instance.save()
                                            
                                    facility_results.append(data_dict)
                    else:
                        return Response({"message": "실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            results.append({code_name: facility_results})
        return Response({"results": results}, status=status.HTTP_200_OK)


class FacilityAddressAPIView(APIView):
    def get(self, request):
        facilities = Facility.objects.all()
        addresses = [facility.address for facility in facilities]
        return Response({'addresses':addresses})

def home(request):
    return render(request, 'map/home.html')
def test(request):
    return render(request, 'map/facility.html')