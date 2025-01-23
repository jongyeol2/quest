from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, CommentAPIView, CommentUDAPIView, PostLikeAPIView


app_name = "posts"
urlpatterns = [
    path("", PostListAPIView.as_view(), name="post_list"),
    path("<int:post_pk>/", PostDetailAPIView.as_view(), name="post_detail"),
    path("<int:post_pk>/", PostDetailAPIView.as_view(), name="post_detail"),
    path("<int:post_pk>/like/", PostLikeAPIView.as_view(), name="post_like"),
    
    path("<int:post_pk>/comments/", CommentAPIView.as_view(), name="comment"),
    path("<int:post_pk>/comments/<int:comment_pk>/", CommentUDAPIView.as_view(), name="comment_ud"),
]
