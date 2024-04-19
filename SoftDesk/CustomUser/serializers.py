from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "age",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["id", "is_active", "is_staff", "date_joined"]
        extra_kwargs = {
            "username": {"required": True},
            "age": {"required": True},
            "can_be_contacted": {"required": False},
            "can_data_be_shared": {"required": False},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit comporter au moins 8 caractères")
        return value

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Le nom d'utilisateur doit comporter au moins 4 caractères")
        return value

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
