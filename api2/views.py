from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Tag

from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from .serializers import UserSerializer, PostSerializer, PostListSerializer, PostRetrieveSerializer, CommentSerializer, CatetagSerializer, PostSerializerDetail

from collections import OrderedDict

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            ('postList', data)
        ]))
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()
        data = {
            "post" : instance,
            "prevPost" : prevInstance,
            "nextPost" : nextInstance,
            "commentList" : commentList,
        }
        serializer = PostSerializerDetail(instance = data)
        return Response(serializer.data)
    
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)
    
    def get_serializer_context(self):

        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):

        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail

    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()
        data = {
            "post" : instance,
            "prevPost" : prevInstance,
            "nextPost" : nextInstance,
            "commentList" : commentList,
        }
        serializer = self.get_serializer(instance = data)
        return Response(serializer.data)

    def get_serializer_context(self):

        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except:
        prev = None
    
    try:
        nextt = instance.get_next_by_update_dt()
    except:
        nextt = None

    return prev, nextt
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()
    #serializer_class = PostListSerializer

    #def update(self, request, *args, **kwargs):
    #    partial = kwargs.pop('partial', False)
    #    instance = self.get_object()
    #    data = {"like" : instance.like +1}
    #    serializer = self.get_serializer(instance, data=data, partial=partial)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_update(serializer)
#
    #    if getattr(instance, '_prefetched_objects_cache', None):
    #        # If 'prefetch_related' has been applied to a queryset, we need to
    #        # forcibly invalidate the prefetch cache on the instance.
    #        instance._prefetched_objects_cache = {}
#
    #    return Response(data['like'])

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)

@permission_classes((permissions.AllowAny,))    
class CatetagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            "cateList" : cateList,
            "tagList" : tagList,
        }

        serializer = CatetagSerializer(instance = data)
        return Response(serializer.data)

    
