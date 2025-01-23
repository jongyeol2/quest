from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status


class PostListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  
        return [IsAuthenticated()]
    
    def get(self, request):
        posts = Post.objects.all().order_by("-pk")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  
        return [IsAuthenticated()]
    
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        if post.author != request.user:
            return Response(
                {"error": "작성자만 수정가능합니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        if post.author != request.user:
            return Response(
                {"error": "작성자만 삭제가능합니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
            message = "좋아요 취소"
        else:
            post.like_users.add(request.user)
            message = "좋아요 성공"
        totla_like = post.like_users.count()
        return Response(
            {"message": message, "총 좋아요 갯수": totla_like},
            status=status.HTTP_200_OK
        )


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUDAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, post_pk, comment_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_pk, post=post)
        if comment.author != request.user:
            return Response(
                {"error": "작성자만 수정가능합니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, post_pk, comment_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_pk, post=post)
        if comment.author != request.user:
            return Response(
                {"error": "작성자만 삭제가능합니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










