from django.urls import path, include

from rest_framework import routers

from .views import MemberViewSet

router = routers.DefaultRouter()
router.register('member', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
