from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("stu1", views.StudentModelViewSet,)
router.register("stu2", views.Home4APIView,)
router.register("stu3", views.Home5APIView,)


urlpatterns = [
    path("", include(router.urls)),
    path("s1/", views.HomeAPIView.as_view()),

]