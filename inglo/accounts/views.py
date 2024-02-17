import logging
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

logger = logging.getLogger('django')
logger.info("Starting the application...")

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
