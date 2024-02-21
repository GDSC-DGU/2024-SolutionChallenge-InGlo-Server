from django.urls import path
from django.conf.urls import include
from accounts.views import (
    # GoogleLoginView,
    CustomGoogleLoginView,
    ProfileImageUploadView,
    UserDetailViewSet,
    CustomTokenRefreshView,
    AdditionalInfoProvidedView,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('dj_rest_auth.registration.urls')),
    path('', include('allauth.urls')),
    # path('google/login/', GoogleLoginView.as_view(), name='api_accounts_google_oauth'), # api 테스트용
    path('loginsuccess/', CustomGoogleLoginView.as_view(), name='custom_google_login'), # 배포 환경 용
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # path('login-success/', GoogleLoginView.get_response, name='login-success'),
    path('info/', UserDetailViewSet.as_view({'get':'retrieve','patch':'update'}), name='user-info'),
    path('info/profile-img/', ProfileImageUploadView.as_view(), name='profile_image_upload'),
    path('additional-info/', AdditionalInfoProvidedView.as_view(), name='additional-info'),
]