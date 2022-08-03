from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


# APIView是drf中提供的所有视图类的基类，它继承于django.views.view
# 如果视图累直接或简介继承了drf提供的apiview，则我们在视图中调用的request对象活着返回的response都要和django进行区分
class Student2APIView(APIView):

    def get1(self, request):
        print(f"request={request}")
        return Response({"msg": "ok"})

    def get2(self, request):
        """drf提供的request对象的常用操作"""
        # print(request.user) #获取本次的登陆用户模型对象，如果客户端没有登陆，则返回一个相当于none的匿名用户对象
        # print(request.user.id)
        print(request.query_params)  # 获取地址栏上面的查询字符串 ？后面的数据，就是原来django里面的request.GET
        # print(request.data) 获取请求体数据，相当于原来django里面的post和body的组合
        # print(request.files) 获取上传文件列表
        return Response({"msg": "ok"})

    def post(self, request):
        print(request.data)  # 获取请求体数据，相当于原来django里面的post和body的组合
        # print(request.files) 获取上传文件列表
        print(request._request.META)
        return Response({"msg": "ok"})

    def get(self, request):
        """"响应数据"""
        data = {"msg": "ok"}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")