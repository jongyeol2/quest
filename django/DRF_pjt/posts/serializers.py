from rest_framework import serializers
from .models import Post, Comment
from rest_framework.fields import CurrentUserDefault


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post", "author", )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    like_users = serializers.StringRelatedField(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", ]
    
    def get_total_likes(self, obj):
        return obj.like_users.count()


