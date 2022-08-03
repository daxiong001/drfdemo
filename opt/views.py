from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from opt.pagination import Home5PageNumberPagination
from restful.serializers import StudentModelSerializer
from rsd.authentication import CustomerAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from restful.models import Student
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class HomeAPIView(APIView):
    # authentication_classes = [CustomerAuthentication]

    def get(self, request):
        """单独认证"""
        print(request.user)
        print(AnonymousUser)
        if request.user.id is None:
            return Response("未登录:游客")
        else:
            return Response(f"已登陆用户：{request.user}")


class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class Home3APIView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        return Response("访问了视图")


class Home4APIView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    # 局部设置 在指定的视图设置过滤
    # filter_backends = [DjangoFilterBackend]
    filter_fields = ["sex", "classmate"]
    #   list方法中进行调用-》调用了genericAPIView中声明的filter_queryset方法-》配置过滤器类的filter_queryset-》filter_fields

    # 排序
    ordering_fields = ["age", 'id']


class Home5APIView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    #   局部分页
    pagination_class = Home5PageNumberPagination

    # pagination_class = None #关闭分页功能，list会自动默认分页

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
