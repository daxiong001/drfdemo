from django.shortcuts import render
from django.views import View
from restful.models import Student
from .serializers import StudentSerializer, StudentModelSerializer
from django.http.response import JsonResponse


class Student1View(View):

    def get1(self, request):
        """使用序列化器对数据进行序列化格式转换，提供给客户端使用"""

        """序列化一条数据"""
        # 对数据查询
        student = Student.objects.first()
        """实力话序列化器得到序列化器对象"""
        # serializer = StudentSerializer(instance=需要转换格式数据的模型类/查询集【多个],
        # data = 需要进行转换的数据，来自客户端提交过来的字典/列表,
        # context = {} 需要从试图中传递给序列化器使用的其他第三方数据,
        # many=设置本次转换的数据是否为多条数据，决定了序列化器是否使用for循环来进行数据转换，true/false)

        # 查询一条数据
        # serializer = StudentSerializer(instance=Student)
        # 查询多条数据
        # serializer = StudentSerializer(instance=student_list, many=True)
        # 更新一条数据
        # serializer = StudentSerializer(instance=Student, data=data)
        # 添加一条数据
        # serializer = StudentSerializer(data=data)
        # 删除一条数据,一般不需要使用序列化器转换
        serializer = StudentSerializer(student)
        return JsonResponse(serializer.data)

    def get2(self, request):
        """序列化多条数据 """
        student_list = Student.objects.all()
        serializer = StudentSerializer(instance=student_list, many=True)
        """OrdererDict是python内置的高级数据类型，叫有序字典，主要为了解决基本数据类型的dict在存储数据时的随机性问题"""
        return JsonResponse(serializer.data, safe=False)

    def get3(self, request):
        data = {
            "name": "王小明",
            "age": 17,
            "sex": 1,
            "classmate": 301,
            "user": "root"
        }
        serializer = StudentSerializer(data=data)
        # raise_exception=true表示在反序列化验证数据失败以后，由drf直接跑出异常，返回错误提示给客户端
        # serializer.is_valid(raise_exception=True)
        ret = serializer.is_valid()
        if ret:
            print(f"serializer.validated_data={serializer.validated_data}")
        else:
            print(f"serializer.errors={serializer.errors}")

        return JsonResponse({"msg": "ok"})

    def get4(self, request):
        data = {
            "name": "tom",
            "age": 30,
            "sex": 3,
            "classmate": 501
        }
        serializer = StudentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({"msg": "ok"})

    def get5(self, request):
        """ 添加 """
        params = {
            "name": "tom",
            "age": 30,
            "sex": 1,
            "classmate": 201,
            "description": "测试描"
        }
        serializer = StudentSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        # 3、调用save方法调用模型存储数据
        # 此处的save是序列化器内部的save方法，不是模型使用的save方法
        student = serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)

    def get6(self, request):
        """更新"""
        pk = 8
        params = {
            "name": "更新1",
            "age": 30,
            "sex": 1,
            "classmate": 201,
            "description": "测试描"
        }
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(instance=student, data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)

    def get(self, request):
        """在特殊也无暇，可以让客户端绕过部分字段的验证，仅针对客户端提交的数据进行验证"""
        pk = 7
        params = {"age": 55}
        student = Student.objects.get(pk=pk)
        #   partial=true 设置只验证有值的字段
        serializer = StudentSerializer(instance=student, data=params, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)


class Student2View(View):

    def get1(self, request):
        """序列化一条"""
        student = Student.objects.first()
        serializer = StudentModelSerializer(instance=student)
        print(serializer.data)
        return JsonResponse(serializer.data)

    def get2(self, request):
        """序列化多条"""
        student = Student.objects.all()
        serializer = StudentModelSerializer(instance=student, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    def get3(self, request):
        """添加数据是的反序列化/一般步骤/"""
        params = {
            "name": "王11",
            "age": 100,
            "sex": 1,
            "classmate": 30111
        }
        serializer = StudentModelSerializer(data=params)
        # raise_exception=true表示在反序列化验证数据失败以后，由drf直接跑出异常，返回错误提示给客户端
        # serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    def get(self, request):
        """模型序列化更新"""
        pk = 8
        params = {
            "name": "更新3",
            "age": 30,
            "sex": 1,
            "classmate": 201,
            "description": "测试描",
            "user": "root"
        }
        student = Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(instance=student, data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)
