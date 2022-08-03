from django.shortcuts import render
from .models import Teacher, Course, Student
from .serializers import TeacherModelSerializer, Course2ModelSerializer, StudentSerializer,Student2Serializer
from django.views import View
from django.http.response import JsonResponse


# Create your views here.

class TeacherView(View):

    def get1(self, request):
        """获取一个老师信息"""
        teacher = Teacher.objects.first()
        serializer = TeacherModelSerializer(instance=teacher)
        return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})

    def get(self, request):
        """获取多个老师信息"""
        teacher = Teacher.objects.all()
        serializer = TeacherModelSerializer(instance=teacher, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={"ensure_ascii": False})


class CourseView(View):

    def get1(self, request):
        """获取一个课程信息"""
        course = Course.objects.first()
        serializer = Course2ModelSerializer(instance=course)

        return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})

    def get(self, request):
        """获取多个个课程信息"""
        course = Course.objects.all()
        serializer = Course2ModelSerializer(instance=course, many=True)

        return JsonResponse(serializer.data, safe=False, json_dumps_params={"ensure_ascii": False})


class StudentView(View):
    """指定层级"""
    def get1(self, request):
        student = Student.objects.first()
        serializer = StudentSerializer(instance=student)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={"ensure_ascii": False})

    """自定义模型属性方法"""
    def get(self, request):
        student = Student.objects.first()
        serializer = Student2Serializer(instance=student)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={"ensure_ascii": False})
