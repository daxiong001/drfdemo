from django.urls import path
from . import views

urlpatterns = [
    path("s1/", views.Student2APIView.as_view())
]