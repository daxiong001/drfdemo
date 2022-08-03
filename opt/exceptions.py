from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def customer_exception_handler(exc, context):
    """
    :param exc: 发生宜昌市，异常实例对象
    :param context: 字典，异常发生时python解析器手机的执行上下文信息,执行上下文就是python解释器执行代码时保存在内存中的变量
    、函数、类、对象、模块等一系列的信息组成的环境信息
    :return:
    """
    response = exception_handler(exc, context)
    if response is None:
        return Response({
            'message': '服务器错误:{exc}'.format(exc=exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        # print('123 = %s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'message': '服务器错误:{exc}'.format(exc=exc),
        }, status=response.status_code, exception=True)


