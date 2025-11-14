from users.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "city",
            "password",
            "email",
            "avatar",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"), password=validated_data["password"]
        )
        return user
