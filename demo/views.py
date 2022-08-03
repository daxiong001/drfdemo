from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import StudentModelSerializer
from restful.models import Student
from rest_framework.views import APIView, status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, \
    UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet


# Create your views here.

class StudentListAPIView(APIView):

    def get(self, request):
        """获取多条数据"""
        student_list = Student.objects.all()
        serializer = StudentModelSerializer(instance=student_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        """新增一条数据"""
        serializer = StudentModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoAPIView(APIView):

    def get(self, request, pk):
        """获取一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentModelSerializer(instance=student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """更新一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentModelSerializer(instance=student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """删除一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)


"""
APIView中的api接口代码，除了部分涉及到调用模型和序列化器的代码以外，其他代码几乎都是固定写法。
所以，当我们将来针对增删查改的通用api接口编写时，完全可以基于原有的代码进行复用，
那么，drf也考虑到了这个问题，所以提供了一个genericAPIView（通用视图类），让我们可以把接口中独特的代码单独提取出来作为属性存在。
rest_framework.generic.genericAPIView是APIView的子类，在APIView的基础上进行属性扩展提供了2个属性，4个方法，方便我们针对通用接口
"""


class StudentList2GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfo2GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        # student = self.get_queryset().get(pk=pk)
        student = self.get_object()  # 上一个注释的简写获取到当前为pk的对象
        serializer = self.get_serializer(instance=student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object()
        serializer = self.get_serializer(instance=student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
使用通用视图类结合Mixins混入类【扩展类】来实现通用api接口的编写
from rest_framework.mixins import ListModelMixin 获取多条数据，返回响应结果 list
from rest_framework.mixins import CreateModelMixin 添加一条数据，返回响应结果    create
from rest_framework.mixins import RetrieveModelMixin 获取一条数据，返回响应结果  Retrieve
from rest_framework.mixins import UpdateModelMixin 更新一条数据，返回响应结果  update(更新所有字段)和partial_update（更新部分字段）
from rest_framework.mixins import DestroyModelMixin 删除一条数据，返回响应结果  destroy
"""


class StudentList3GenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        """获取多条数据"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """添加数据"""
        return self.create(request, *args, **kwargs)


class StudentInfo3GenericAPIView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        """获取一条数据"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """更新一条数据"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """删除一条数据"""
        return self.destroy(request, *args, **kwargs)


"""
上面这些接口代码还可以继续更加的精简，drf在使用GenericAPIView和Mixins进行组合以后，还提供了视图子类
这些视图子类，提供了各种的视图方法调用mixins操作
ListAPIView = GenericAPIView  +   ListModelMixin    获取多条数据的视图方法
CreateAPIView = GenericAPIView  +   CreateModelMixin    新增一条数据的视图方法
RetrieveAPIView = GenericAPIView  +   RetrieveModelMixin    查询一条数据的视图方法
UpdateAPIView = GenericAPIView  +   UpdateModelMixin    更新一条数据的视图方法
DestroyAPIView = GenericAPIView  +   DestroyModelMixin    删除一条数据的视图方法

组合视图类
ListCreateAPIView,
RetrieveUpdateDestroyAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
"""


class StudentList4GenericAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class StudentInfo4GenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
针对视图子类这种写法虽然省略了http请求，但是在开发通用五个api接口时，还是会出现需要两个类来实现5个接口
主要原因是：
1、获取多条数据与获取一条数据的http请求重复了，在django中依赖于请求方法来响应不同的http请求
2、部分接口需要pk值作为url地址

drf为了解决上面的两个问题，提供了视图集和路由集。
视图集就可以帮我们实现一个视图类响应多种重复的http请求
ViewSet路由集就可以帮我们实现自动根据不同的视图方法来生成不同参数的路由地址
"""


class StudentViewSet(ViewSet):

    def get_one(self, request, pk):
        """获取一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentModelSerializer(instance=student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)

    def get_all(self, request):
        instance = Student.objects.all()
        serializer = StudentModelSerializer(instance=instance, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StudentModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """更新一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentModelSerializer(instance=student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)

    def destory(self, request, pk):
        """删除一条数据"""
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"msg": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)


"""
GenericViewSet抽离独特代码更方便
"""


class StudentGenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_all(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_one(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


"""
GenericViewSet结合Mixins的混入类，直接视图接口，这次连视图子类都不需要了
"""


class StudentMixinViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
                          RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class StudentAllViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    @action(methods=["get", "post"], detail=False, url_path="user_login")
    def login(self, request):
        return Response({"msg": "ok"})
