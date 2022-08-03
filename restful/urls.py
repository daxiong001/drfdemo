from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

urlpatterns = [

]

router = DefaultRouter()
router.register("stu", viewset=views.StudentModelViewSet, basename="stu")
urlpatterns += router.urls