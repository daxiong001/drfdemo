from django.urls import path
from . import views


urlpatterns = [
    path("s1/", views.Student1View.as_view()),
    path("s2/", views.Student2View.as_view()),
]
