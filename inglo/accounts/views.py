import logging
import requests
import secrets
from dotenv import load_dotenv
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenError
from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .services.user_service import UserService

logger = logging.getLogger('django')
logger.info("Starting the application...")
load_dotenv()
    
User = get_user_model()

class CustomGoogleLoginView(views.APIView):

    authentication_classes = []  
    permission_classes = []

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        if not access_token:
            return JsonResponse({"error": "Access token is required"}, status=400)

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

        refresh_token = RefreshToken.for_user(user)
        user.refresh_token = str(refresh_token)
        user.save()

        response_data = {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token),
        }

        return JsonResponse(response_data)
    
class CustomTokenRefreshView(TokenRefreshView):

    authentication_classes = []  
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        # 리프레시 토큰의 유효성과 유효 기간 검증
        try:
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token['user_id'], refresh_token=refresh_token)

            # 새로운 리프레시 토큰과 액세스 토큰 발급
            refresh_token = RefreshToken.for_user(user)
            user.refresh_token = str(refresh_token)
            user.save()

            response_data = {
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token),
            }
            return JsonResponse(response_data)
        except TokenError:
            return JsonResponse({"error": "Invalid or expired refresh token"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    
class ProfileImageUploadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        유저가 업로드한 프로필 이미지를 S3에 저장하고, 이미지 URL을 유저 모델에 저장
        """
        user = request.user
        image = request.FILES.get('image')  # 'profile_img'는 form-data에서 파일 필드의 이름
        if not image:
            return JsonResponse({"error": "No image provided"}, status=400)

        user = UserService.update_user_profile_image(user, image)
        if not user:
            return JsonResponse({"error": "Profile image upload failed"}, status=400)

        return JsonResponse({"message": "Profile image uploaded successfully"})

class UserDetailViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin):
    """
    유저 정보 조회
    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        UserService.update_global_impact(user)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('name')
        country = request.data.get('country')
        language = request.data.get('language')
        if UserService.update_user_info(user, name, country, language):
            return JsonResponse({"message": "User information updated successfully"}, status=200)
        else:
            return JsonResponse({"error": "User information update failed"}, status=400)
        
class AdditionalInfoProvidedView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info("access_token: " + request.headers.get('Authorization'))
        user = request.user
        return JsonResponse({"additional_info_provided": user.additional_info_provided})

