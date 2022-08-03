from django.urls import path
from . import views

urlpatterns = [
    path("s1/", views.TeacherView.as_view()),
    path("s2/", views.CourseView.as_view()),
    path("s3/", views.StudentView.as_view()),
]
