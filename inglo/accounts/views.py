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

    def post(self, request, *args, **kwargs):
        user = request.user
        image = request.FILES.get('profile_img')  # 'profile_img'는 form-data에서 파일 필드의 이름
        if not image:
            return JsonResponse({"error": "No image provided"}, status=400)

        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        file_path = f'user_{user.id}/{image.name}'  # S3 내에서 파일을 저장할 경로
        s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ACL='public-read')

        image_url = f'https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}'
        user.profile_img = image_url
        user.save()

        return JsonResponse({"message": "Profile image uploaded successfully", "image_url": image_url})

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
