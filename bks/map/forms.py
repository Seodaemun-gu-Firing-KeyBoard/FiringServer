from django import forms
from .models import *

# class FacilityForm(forms.ModelForm):
#     class Meta:
#       model = Facility
#       fields = ["name","location","target","use","reception","select","recruit","application","fee","reserve","call","image"]
#       labels = {
#          "name": "시설명",
#          "location": "위치",
#          "target": "대상",
#          "use": "이용기간",
#          "reception": "접수기간",
#          "select": "선별방법",
#          "recruit": "모집정원",
#          "application": "신청제한",
#          "fee": "이용요금",
#          "reserve": "예약방법",
#          "call": "문의전화",
#          "image": "이미지",
      # }