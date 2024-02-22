from django.http import HttpResponseForbidden
import os
from dotenv import load_dotenv
from logging import getLogger
logger = getLogger('django')
load_dotenv()

def allow_server_ip_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        logger.info('client IP: ' + request.META['REMOTE_ADDR'])
        my_ip = os.getenv('MYIP')
        my_ip2 = os.getenv('MYIP2')
        logger.info('my IP: ' + my_ip)
        allowed_ips = ['127.0.0.1', my_ip, my_ip2 ]  # 허용할 IP 주소
        if request.META['REMOTE_ADDR'] not in allowed_ips:
            return HttpResponseForbidden("Access denied.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func