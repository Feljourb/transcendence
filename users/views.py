from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistreSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegistreView(APIView):
    def post(self, request):
        serializer = RegistreSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save() 
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user) 
        return Response(serializer.data) 

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        try:
            refresh_token = request.data["refresh"] 
            token = RefreshToken(refresh_token) 
            token.blacklist() 
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
