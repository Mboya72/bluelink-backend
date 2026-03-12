from rest_framework import serializers
from .models import User, FishermanProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

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