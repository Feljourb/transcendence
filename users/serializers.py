from rest_framework import serializers 
from .models import User 

class RegistreSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True) 

	class Meta:
		model = User 
		fields = ('username', 'password', 'email', 'bio', 'location', 'skills') 

	def create(self, validated_data):
		user = User.objects.create_user(
			username=validated_data['username'],
			password=validated_data['password'],
			email=validated_data.get('email', ''),
			bio=validated_data.get('bio', ''),
			location=validated_data.get('location', ''),
			skills=validated_data.get('skills', '')
		) 
		return user 

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User 
		fields = ('username', 'email', 'bio', 'location', 'skills') 
