from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                {
                    "message": "회원가입 완료!",
                    "ID": user.username,
                    "bio": user.bio,
                    "image": user.image.url + " (추후에 S3 이용해 url 반환 예정)",
                },
                status=status.HTTP_201_CREATED
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {
                        "message": "로그아웃 실패",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                "message": "로그아웃 완료!",
            },
            status=status.HTTP_204_NO_CONTENT
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class DeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        request.user.delete()
        return Response(
            {
                "message": "회원탈퇴 완료!",
            },
            status=status.HTTP_204_NO_CONTENT
        )



