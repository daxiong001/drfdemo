from django.db import models
from django.utils import timezone as datetime


class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=False)

    class Meta:
        db_table = "sch_student"
        verbose_name = "学生表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    """自定义模型属性"""
    @property
    def achievement(self):
        queryset = self.s_achievement.all()
        ret = [{"score": item.score, "course": item.course.name, "teacher": item.course.teacher.name} for item in queryset]
        return ret


class Teacher(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=50)
    sex = models.BooleanField(default=False, verbose_name="性别")

    class Meta:
        db_table = "sch_teacher"
        verbose_name = "老师表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名称")
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, related_name="course", db_constraint=False)

    class Meta:
        db_table = "sch_course"
        verbose_name = "课程表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Achievement(models.Model):
    score = models.DecimalField(default=0, max_digits=4, decimal_places=1, verbose_name="成绩")
    student = models.ForeignKey("Student", on_delete=models.DO_NOTHING, related_name="s_achievement",
                                db_constraint=False)
    course = models.ForeignKey("Course", on_delete=models.DO_NOTHING, related_name="c_achievement", db_constraint=False)
    create_time = models.DateTimeField(auto_created=datetime.now)

    class Meta:
        db_table = "db_achievement"
        verbose_name = "成绩表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(float(self.score))
