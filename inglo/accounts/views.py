import logging
import boto3
import os
import magic
import requests
import secrets
from dotenv import load_dotenv
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .services.user_service import UserService

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
        logger.info(f"CustomGoogleLoginView.post() called with access_token: {access_token}")
        if not access_token:
            return JsonResponse({"error": "Access token is required"}, status=400)

        # Google 사용자 정보 엔드포인트
        info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        response = requests.get(info_url, params={'access_token': access_token})
        user_info = response.json()

        if "error" in user_info:
            return JsonResponse({"error": "Failed to fetch user information from Google"}, status=400)

        user, created = User.objects.get_or_create(email=user_info['email'])

        # 새로운 사용자의 경우 임의의 비밀번호 설정
        if created:
            random_password = secrets.token_urlsafe()
            user.set_password(random_password)
            user.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return JsonResponse(response_data)
    
class AdditionalUserInfoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.name = request.data.get('name')
        user.country = request.data.get('country')
        user.language = request.data.get('language')
        user.additional_info_provided = True
        user.save()
        return JsonResponse({"message": "Additional user information updated successfully"}, status=200)
    
class ProfileImageUploadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        유저가 업로드한 프로필 이미지를 S3에 저장하고, 이미지 URL을 유저 모델에 저장
        """
        user = request.user
        image = request.FILES.get('profile_img')  # 'profile_img'는 form-data에서 파일 필드의 이름
        if not image:
            return JsonResponse({"error": "No image provided"}, status=400)

        user = UserService.upload_profile_image(user, image)
        if not user:
            return JsonResponse({"error": "Profile image upload failed"}, status=400)

        return JsonResponse({"message": "Profile image uploaded successfully"})

class UserDetailView(views.APIView):
    """
    유저 정보 조회
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        UserService.update_global_impact(user)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

class UserUpdateView(views.APIView):
    """
    유저 정보 수정
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('name')
        country = request.data.get('country')
        language = request.data.get('language')
        if UserService.update_user_info(user, name, country, language):
            return JsonResponse({"message": "User information updated successfully"}, status=200)
        else:
            return JsonResponse({"error": "User information update failed"}, status=400)
