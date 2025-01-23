from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "password", "bio", ]
    
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            # image=validated_data.get("image", ""),
        )
        if image:
            user.image = image
            user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "bio", ]