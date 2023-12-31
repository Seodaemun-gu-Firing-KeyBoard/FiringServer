import os
import requests
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponseRedirect, JsonResponse
from requests import JSONDecodeError
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from dj_rest_auth.registration.views import SocialLoginView
from .models import CustomUser
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from allauth.account.utils import send_email_confirmation
from .serializers import CustomUserSerializer, CustomUserDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'api/auth/kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'api/auth/naver/callback/'


# 회원 탈퇴
class CustomDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 회원 정보 조회, 수정
class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserDetailsSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user


# 액세스,리프레쉬 토큰 재발급
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 현재 리프레쉬 토큰에서 사용자 정보 가져오기
        current_refresh_token = RefreshToken(attrs['refresh'])
        user_id = current_refresh_token["user_id"]

        # CustomUser 객체 찾기
        CustomUser = get_user_model()
        current_user = CustomUser.objects.get(pk=user_id)

        # 새로운 리프레쉬 토큰 생성 및 추가
        new_refresh_token = RefreshToken.for_user(current_user)
        data['refresh'] = str(new_refresh_token)

        return data


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


# 회원가입
class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_email_confirmation(self.request, user)

    def create(self, request, *args, **kwargs):
        response = super(RegisterView, self).create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {
                "message": "이메일 전송을 완료했습니다. 이메일을 확인해주세요."
            }
        return response


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/')  # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/')  # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email,profile_nickname")


def kakao_callback(request):
    try:
        client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        code = request.GET.get("code")

        # code로 access token 요청
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
        token_response_json = token_request.json()

        # 에러 발생 시 중단
        error = token_response_json.get("error", None)
        if error is not None:
            raise JSONDecodeError(error)

        access_token = token_response_json.get("access_token")

        #################################################################
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print(profile_json)

        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        nickname = profile_json.get("properties").get("nickname", None)

        if email is None:
            return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        if nickname is None:
            return JsonResponse({'err_msg': 'failed to get nickname'},
                                status=status.HTTP_400_BAD_REQUEST)  # 닉네임 확인용 에러 메시지 추가
        # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
        try:
            # 전달받은 이메일로 등록된 유저가 있는지 탐색
            user = CustomUser.objects.get(email=email)

            # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != 'kakao':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

            data = {'access_token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/auth/kakao/login/finish/", data=data)
            accept_status = accept.status_code

            # 뭔가 중간에 문제가 생기면 에러
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)

        except CustomUser.DoesNotExist:
            # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급

            data = {'access_token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/auth/kakao/login/finish/", data=data)
            accept_status = accept.status_code

            # 뭔가 중간에 문제가 생기면 에러
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            else:
                user = CustomUser.objects.get(email=email)
                user.username = email
                user.email = email
                user.nickname = nickname
                user.save()

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)
    except SocialAccount.DoesNotExist:
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


class NaverLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
        return redirect(
            f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URI}")


def naver_callback(request):
    try:
        client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_NAVER_SECRET")
        code = request.GET.get("code")
        state_string = request.GET.get("state")

        # code로 access token 요청
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state_string}")
        token_response_json = token_request.json()

        # 에러 발생 시 중단
        error = token_response_json.get("error", None)
        if error is not None:
            raise JSONDecodeError(error)

        access_token = token_response_json.get("access_token")

        #################################################################
        profile_request = requests.post(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        naver_account = profile_json.get("response")
        email = naver_account.get("email", None)
        nickname = naver_account.get("nickname", None)

        if email is None:
            return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        if nickname is None:
            return JsonResponse({'err_msg': 'failed to get nickname'},
                                status=status.HTTP_400_BAD_REQUEST)  # 닉네임 확인용 에러 메시지 추가
        # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
        try:
            # 전달받은 이메일로 등록된 유저가 있는지 탐색
            user = CustomUser.objects.get(email=email)

            # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != 'naver':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

            data = {'access_token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/auth/naver/login/finish/", data=data)
            accept_status = accept.status_code

            # 뭔가 중간에 문제가 생기면 에러
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)

        except CustomUser.DoesNotExist:
            # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급

            data = {'access_token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/auth/naver/login/finish/", data=data)
            accept_status = accept.status_code
            print(accept_status + 10000)

            # 뭔가 중간에 문제가 생기면 에러
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            else:
                user = CustomUser.objects.get(email=email)
                user.username = email
                user.email = email
                user.nickname = nickname
                user.save()

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)
    except SocialAccount.DoesNotExist:
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client

class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)