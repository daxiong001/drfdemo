from rest_framework import serializers

from school.models import Teacher, Course, Student


class CourseModelSerializer(serializers.ModelSerializer):
    courseName = serializers.CharField(source="name")

    class Meta:
        model = Course
        fields = ["id", "courseName"]


"""一对多"""


class TeacherModelSerializer(serializers.ModelSerializer):
    # 1、重写模型对应的外键，指定返回的数据是什么
    course = CourseModelSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ["id", "name", "course"]


"""多对一或一对一"""


class Teacher2ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "name"]


class Course2ModelSerializer(serializers.ModelSerializer):
    # 1、第一种方式，嵌套查找外间全部信息
    # teacher = Teacher2ModelSerializer()
    # 2、第二种方式，指定字段
    # teacher = serializers.CharField(source="teacher.name")

    class Meta:
        model = Course
        fields = ["id", "name", "teacher"]
        # 3、第三种，指定查询深度
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    # 层级查询外键
    class Meta:
        model = Student
        fields = ["id", "name", "s_achievement"]
        depth = 3


class Student2Serializer(serializers.ModelSerializer):
    """自定义模型属性方法"""
    class Meta:
        model = Student
        fields = ["id", "name", "achievement"]
