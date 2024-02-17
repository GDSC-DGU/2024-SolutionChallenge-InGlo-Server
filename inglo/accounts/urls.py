from django.urls import path
from django.conf.urls import include
from accounts.views import (
    GoogleLoginView,
    # KakaoLoginView,
    # NaverLoginView,
)
from accounts.views import UserDetailView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('dj_rest_auth.registration.urls')),
    path('', include('allauth.urls')),
    # path('kakao/login/', KakaoLoginView.as_view(), name='api_accounts_kakao_oauth'),
    path('google/login/', GoogleLoginView.as_view(), name='api_accounts_google_oauth'),
    # path('naver/login/', NaverLoginView.as_view(), name='api_accounts_naver_oauth'),
    path('login-success/', GoogleLoginView.get_response, name='login-success'),
    path('info/', UserDetailView.as_view(), name='user-info'),
]