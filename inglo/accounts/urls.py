from django.urls import path
from django.conf.urls import include
from accounts.views import (
    GoogleLoginView,
    CustomGoogleLoginView,
    AdditionalUserInfoView,
    ProfileImageUploadView,
    # KakaoLoginView,
    # NaverLoginView,
)
from accounts.views import UserDetailView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('dj_rest_auth.registration.urls')),
    path('', include('allauth.urls')),
    # path('google/login/', GoogleLoginView.as_view(), name='api_accounts_google_oauth'), # api 테스트용
    path('api/accounts/google/login/', CustomGoogleLoginView.as_view(), name='custom_google_login'), # 배포 환경 용
    path('login-success/', GoogleLoginView.get_response, name='login-success'),
    path('api/accounts/additional_info/', AdditionalUserInfoView.as_view(), name='additional_info'),
    path('api/accounts/profile-image-upload/', ProfileImageUploadView.as_view(), name='profile_image_upload'),
    path('info/', UserDetailView.as_view(), name='user-info'),
    # path('kakao/login/', KakaoLoginView.as_view(), name='api_accounts_kakao_oauth'),
    # path('naver/login/', NaverLoginView.as_view(), name='api_accounts_naver_oauth')
]