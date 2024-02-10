from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/accounts/google/login/callback/'
    client_class = OAuth2Client


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
