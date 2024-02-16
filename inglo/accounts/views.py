from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/accounts/google/login/callback/'
    client_class = OAuth2Client

from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

def login_success(request):
    user = get_user_model().objects.first()  # 실제로는 인증된 사용자를 사용해야 함
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 클라이언트 사이드에서 토큰을 처리할 수 있도록 JsonResponse를 사용하여 토큰 전달
    response_data = {
        'token': access_token
    }

    # JSON 응답 반환
    return JsonResponse(response_data)

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    유저 정보 조회 및 수정
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.request.user

    def get_serializer_context(self):
        return {'request': self.request}


# class KakaoLoginView(SocialLoginView):
#     adapter_class = KakaoOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000/api/accounts/kakao/login/callback/'
#     client_class = OAuth2Client
#
#
# class NaverLoginView(SocialLoginView):
#     adapter_class = NaverOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000/api/accounts/naver/login/callback/'
#     client_class = OAuth2Client
