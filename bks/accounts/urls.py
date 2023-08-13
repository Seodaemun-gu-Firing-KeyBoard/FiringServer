from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include, re_path
from .views import RegisterView
from .views import ConfirmEmailView, kakao_login, kakao_callback, KakaoLogin
from .views import CustomTokenRefreshView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    # access token,refresh token 재발급
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('signup', RegisterView.as_view(), name='signup'),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),

    #oauth-kakao
    path('kakao/login/', kakao_login, name='kakao_login'),
    path('kakao/callback/', kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_finish'),
]
