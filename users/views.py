from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistreSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User

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
        
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        try:
            refresh_token = request.data["refresh"] 
            token = RefreshToken(refresh_token) 
            token.blacklist() 
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT) 
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class PublicProfileView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class SearchBySkillView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        
        if query:
            users = User.objects.filter(
                skills__name__icontains=query
            ).exclude(id=request.user.id).distinct()
        else:
            users = User.objects.none()
            
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class SearchFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('username', '')
        friends = request.user.friends.all()
        
        if query:
            friends = friends.filter(username__icontains=query)
            
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

class ToggleFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        
        if target_user == request.user:
            return Response({"error": "You cannot add yourself as a friend."}, status=400)
            
        if target_user in request.user.friends.all():
            request.user.friends.remove(target_user)
            return Response({"message": f"Removed {username} from friends."})
        else:
            request.user.friends.add(target_user)
            return Response({"message": f"Added {username} to friends."})

