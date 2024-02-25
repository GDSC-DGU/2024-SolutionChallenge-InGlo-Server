from django.http import HttpResponseForbidden
import os
from dotenv import load_dotenv
from logging import getLogger
logger = getLogger('django')
load_dotenv()

def allow_secret_header_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        logger.info('Request received with client IP: ' + request.META['HTTP_X_FORWARDED_FOR'])
        my_ip = os.getenv('MYIP')
        my_ip2 = os.getenv('MYIP2')
        my_ip3 = os.getenv('MYIP3')
        allowed_ips = [my_ip, my_ip2, my_ip3]  # 허용할 IP 주소
        if request.META['HTTP_X_FORWARDED_FOR'] in allowed_ips:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. invalid IP address.")
    return _wrapped_view_func