# 用于解决跨域请求问题
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.deprecation import MiddlewareMixin

class allowCrossDomain(MiddlewareMixin):

    def process_response(self, request, response):
        # 允许跨域请求的地址 (*代表所有地址)
        response['Access-Control-Allow-Origin'] = "http://127.0.0.1:8080"
        # 允许跨域请求的类型
        response['Access-Control-Allow-Headers'] = "X-Requested-With,Content-Type"
        # 允许跨域请求的方式
        response['Access-Control-Allow-Methods'] = "PUT,POST,GET,DELETE,OPTIONS"
        # 允许跨域请求携带cookie
        response['Access-Control-Allow-Credentials'] = "true"

        return response

class CustomSessionmiddleware(SessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get('sessionid')
        if session_key is None:
            session_key = request.META.get('HTTP_AUTHORIZATION')
        request.session = self.SessionStore(session_key)

