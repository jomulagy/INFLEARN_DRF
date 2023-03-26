from django.urls import path, include
from rest_framework import routers

from api2.views import *

# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)

app_name = 'api2'

urlpatterns = [
    #path("",include(router.urls)),
    path("post/",PostViewSet.as_view(actions = {"get" : "list"}),name = "post-list"),
    path("post/<int:pk>/",PostViewSet.as_view(actions = {"get" : "retrieve"}),name = "post-detail"),
    path("comment/",CommentCreateAPIView.as_view(),name = "comment-create"),
    path("post/<int:pk>/like/",PostViewSet.as_view(actions = {"get" : "like"}),name = "post-like"),
    path("catetag/",CatetagAPIView.as_view(), name = "catetag"),
]
    
