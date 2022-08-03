from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

urlpatterns = [
    path("s1/", views.StudentListAPIView.as_view()),
    path("s1/<int:pk>/", views.StudentInfoAPIView.as_view()),
    path("s2/", views.StudentList2GenericAPIView.as_view()),
    path("s2/<int:pk>/", views.StudentInfo2GenericAPIView.as_view()),
    path("s3/", views.StudentList3GenericAPIView.as_view()),
    path("s3/<int:pk>/", views.StudentInfo3GenericAPIView.as_view()),
    path("s4/", views.StudentList4GenericAPIView.as_view()),
    path("s4/<int:pk>/", views.StudentInfo4GenericAPIView.as_view()),
    path("s5/", views.StudentViewSet.as_view(actions={"get": "get_all", "post": "create"})),
    path("s5/<int:pk>/",
         views.StudentViewSet.as_view(actions={"get": "get_one", "put": "update", "delete": "destory"})),

    path("s6/", views.StudentGenericViewSet.as_view(actions={"get": "get_all", "post": "post"})),
    path("s6/<int:pk>/",
         views.StudentGenericViewSet.as_view(actions={"get": "get_one", "put": "update", "delete": "delete"})),

    path("s7/", views.StudentMixinViewSet.as_view(actions={"get": "list", "post": "create"})),
    path("s7/<int:pk>/",
         views.StudentMixinViewSet.as_view(actions={"get": "retrieve", "put": "update", "delete": "destroy"})),

    # path("s8/", views.StudentAllViewSet.as_view(actions={"get": "list", "post": "create"})),
    # path("s8/<int:pk>/",
    #      views.StudentAllViewSet.as_view(actions={"get": "retrieve", "put": "update", "delete": "destroy"})),
]
#   只能添加默认的五个方法
router = DefaultRouter()
router.register("s8", views.StudentAllViewSet, "s8")
urlpatterns += router.urls
