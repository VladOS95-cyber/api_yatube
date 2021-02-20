from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        post = self.get_object()
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def update(self, request):
        post = self.get_object()
        if self.request.user == post.author:
            serializer = self.serializer_class(
                post,
                data=request.data,
                partial=True)
            if serializer.is_valid():
                serializer.save(author=self.request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        post = self.get_object()
        if self.request.user == post.author:
            self.perform_destroy(post)
            return Response(request.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def update(self, request, pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        if request.user == comment.author:
            serializer = self.serializer_class(
                comment,
                data=request.data,
                partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        if request.user == comment.author:
            comment.delete()
            return Response(request.data)
