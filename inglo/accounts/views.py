import logging
import boto3
import os
from dotenv import load_dotenv
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
import requests
import secrets

logger = logging.getLogger('django')
logger.info("Starting the application...")
load_dotenv()

# ----------------------- api 테스트용
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/accounts/google/login/callback/'
    client_class = OAuth2Client

    def get_response(self):
        logger.info("GoogleLoginView.get_response() called")
        user = self.user

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        logger.info(f"JWT Tokens for user {user.email} (ID: {user.id}): {response_data}")

        return JsonResponse(response_data)
    
# ----------------------- api 테스트용
    
User = get_user_model()

class CustomGoogleLoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        if not access_token:
            return JsonResponse({"error": "Access token is required"}, status=400)

        # Google 사용자 정보 엔드포인트
        info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        response = requests.get(info_url, params={'access_token': access_token})
        user_info = response.json()

        if "error" in user_info:
            return JsonResponse({"error": "Failed to fetch user information from Google"}, status=400)

        # 사용자 정보를 바탕으로 사용자 모델 조회 또는 생성
        user, created = User.objects.get_or_create(email=user_info['email'])

        # 새로운 사용자의 경우 임의의 비밀번호 설정
        if created:
            random_password = secrets.token_urlsafe()
            user.set_password(random_password)
            user.save()

        # 사용자에 대한 JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

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
