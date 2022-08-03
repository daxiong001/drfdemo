from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.views import APIView


class CustomerAuthentication(BaseAuthentication):
    """自定义认证"""

    def authenticate(self, request):
        """
        认证方法
        request：本次客户端发过来的http请求
        """
        user = request.query_params.get("user")
        pwd = request.query_params.get("pwd")
        if user != "root" and pwd != "pwd":
            return None
        # get_user_model获取当前系统中用户表对应的用户模型类
        user = get_user_model().objects.get(pk=1)
        return (user, None)
