from django.db import models


class Student(models.Model):
    SEX_OPTION = (
        (0, "保密"),
        (1, "男"),
        (2, "女"),
    )
    name = models.CharField(max_length=20, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄")
    sex = models.SmallIntegerField(choices=SEX_OPTION, verbose_name="性别")
    classmate = models.CharField(db_column="class", max_length=15, verbose_name="班级")
    description = models.TextField(null=True, blank=True, verbose_name="个性签名")

    class Meta:
        db_table = "db_student"
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name
