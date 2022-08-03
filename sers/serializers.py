from rest_framework import serializers
from restful.models import Student


# validators选项的验证函数可以有0到多个，这些验证函数和写在序列化器内部的验证方法使用方法一致，几乎没有区别
# 函数名叫什么无所谓！函数必须有一个参数接收is_valid传递进行的字段数据
# validators是通用的选项，任何字段都可以指定自己多个外部验证函数
# 一般就是验证函数比较通用时，没必要把验证数据代码写在每一个序列化器中的时就可以使用外部验证函数
def check_sex(data):
    if data > 2:
        raise serializers.ValidationError(code="sex", detail="对不起没有这个选项")
    return data


"""基类序列化器"""


class StudentSerializer(serializers.Serializer):
    #   1、申明在请求和响应的过程中，需要进行数据转换的字段
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, min_length=3, max_length=15,
        error_messages={"required": "不能输入为空", "max_length": "长度不能超过15"}
    )
    classmate = serializers.CharField(required=True, max_length=15)
    age = serializers.IntegerField()
    sex = serializers.IntegerField(validators=[check_sex])
    description = serializers.CharField(required=False, max_length=3,
                                        error_messages={"max_length": "长度不能超过3"})

    #   2、如果序列化器继承的是modelSerializer,则需要申明调用的模型

    #   3、验证代码
    #     3.1 对单个字段数据进行验证
    #     格式：
    #         一个序列化器中可以有0个或多个验证方法，方法名唯一
    #         必须以"validate_<字段名>"作为验证方法名，否则is_valid找不到
    #         验证方法执行时，is_valid会把当前客户端提交的字段数据传递到验证方法，我们需要接收该参数进行验证
    #         验证方法必须把当前字段的数据作为方法的返回值，会唱诶序列化器，否则该数据丢失
    def validate_name(self, data):
        print(data)
        if data == "python":
            raise serializers.ValidationError(code="name", detail="当前字段值属于敏感字符")
        #   必须有返回值，而且返回值必须是当前字段的数据值，可以改动数据，但是必须返回
        return data

    # 3.2 对多个字段的数据进行验证
    # 格式:
    #     一个序列化器中只能由0个或1个多字段验证方法，方法名唯一
    #     方法名必须叫validated(self,data),否则is_valid找不到
    #     验证方法执行时，is_valid会把当前客户端提交的所有字段数据传递到验证方法，我们需要接受该参数进行校验
    #     验证方法必须把当前字段的数据作为方法的返回值，回传给序列化器，否则该数据丢失
    def validate(self, attrs):
        age = attrs.get("age")
        classmate = attrs.get("classmate")
        if age < 20 and str(classmate).startswith("5"):
            raise serializers.ValidationError("对不起！年龄在20一下不能添加到5字头班级")
        return attrs

    # 3.3 但字段验证函数，default_validators
    # 在序列化器的字段中添加validators选项参数们也可以补充验证代码
    # 选项validators的值是一个列表，列表的成员必须是一个函数名，这个函数名不能是字符串
    #   4、编写模型的添加和更新代码

    def create(self, validated_data):
        """添加数据，到模型中的实现过程"""
        # 1、无多余字段，直接传字典
        # student = Student.objects.create(**validated_data)
        # 2、如果validated_data有多余的字段，不属于模型对象，则自定义字典
        student = Student.objects.create(
            name=validated_data.get("name"),
            age=validated_data.get("age"),
            sex=validated_data.get("sex"),
            classmate=validated_data.get("classmate"),
            description=validated_data.get("description"),
        )
        #   强烈建议返回添加后的模型对象
        return student

    def update(self, instance, validated_data):
        """更新数据"""
        instance.name = validated_data.get("name")
        instance.age = validated_data.get("age")
        instance.sex = validated_data.get("sex")
        instance.classmate = validated_data.get("classmate")
        #   针对可选字段进行条件判断
        if validated_data.get("description"):
            instance.description = validated_data.get("description")
        instance.save()
        return instance


"""模型类序列化器"""


class StudentModelSerializer(serializers.ModelSerializer):
    #   1、申明要转换的字段【当部分字段不是来自于模型类时，就要自己动手声明】
    user = serializers.CharField(write_only=True)

    #   2、模型类信息
    class Meta:
        model = Student
        fields = ["id", "name", "age", "sex", "classmate", "user"]  # 指定要经过序列化器的字段
        # fields = "__all__"  # 全部字段
        # exclude = ["age"]    排除字段

        # 字段补充说明
        extra_kwargs = {
            "age":
                {"min_value": 0,
                 "max_value": 150,
                 "error_messages": {
                     "min_value": "年龄不能小于0岁",
                     "max_value": "年龄不能大于150岁"
                 }},
            "name":
                {"error_messages": {
                    "max_length": "学生姓名不能超过20个字符！"
                }}
        }

    def validate_user(self, attrs):
        if attrs != "root":
            raise serializers.ValidationError(code="user", detail="只有root用户才能更新")
