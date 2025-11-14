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
        """
        Создание пользователя без кастомного менеджера.
        Корректно хеширует пароль через set_password().
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
