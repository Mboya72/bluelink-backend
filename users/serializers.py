from rest_framework import serializers
from .models import User, FishermanProfile
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'role', 'is_verified_seller', 'bio', 'location', 'profile_picture'
        ]
        # LOCK THE ROLE: The user cannot change these via the profile update
        read_only_fields = ['role', 'is_verified_seller', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', User.Role.BUYER)
        )
        # Automatically create profile based on role
        if user.role == User.Role.FISHERMAN:
            FishermanProfile.objects.create(user=user)
        return user
    
User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 
            'location', 'bio', 'profile_picture', 'phone_number',
            'is_verified_seller'
        ]
        read_only_fields = ['id', 'username', 'email', 'role', 'is_verified_seller']