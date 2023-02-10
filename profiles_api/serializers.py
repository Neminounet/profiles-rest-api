from rest_framework import serializers
from profiles_api import models

# Serializer test
class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing ou APIView"""
    name = serializers.CharField(max_length=10)

# Serializer projet User Profile
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta : 
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password' : {
                'write_only' : True, # pas récupérable en GET uniquement POST ou PUT/PATCH
                'style' : {'input_type' : 'password'} # permet de rendre ****** un password

            }
        }

    # Ecrase les méthodes des viewsets
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

