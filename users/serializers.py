from rest_framework import serializers 
from .models import User, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')

class RegistreSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    skills = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )

    class Meta:
        model = User 
        fields = ('username', 'password', 'email', 'bio', 'location', 'skills', 'avatar') 

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        avatar_data = validated_data.pop('avatar', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            bio=validated_data.get('bio', ''),
            location=validated_data.get('location', ''),
            avatar=avatar_data
        ) 
        
        for skill_name in skills_data:
            skill_obj, created = Skill.objects.get_or_create(name=skill_name.strip().lower())
            user.skills.add(skill_obj)
            
        return user 

class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = User 
        fields = ('username', 'email', 'bio', 'location', 'skills', 'avatar')
