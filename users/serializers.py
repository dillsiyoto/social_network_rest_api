from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from users.models import LoginRecord


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "first_name", 
            "last_name", "email", "password"
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )
        validated_data["is_active"] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(
                validated_data["password"]
            )
        return super().update(instance, validated_data)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if "admin" in value.lower():
            raise serializers.ValidationError("Username cannot contain 'admin'")
        return value

    def validate(self, attrs):
        if attrs["username"] == attrs.get("password"):
            raise serializers.ValidationError("Password cannot be the same as username")
        self.validate_username(value=attrs["username"])
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(
                validated_data["password"]
            )
        return super().update(instance, validated_data)


class LoginConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    ip_address = serializers.IPAddressField()
    code = serializers.CharField()

    def validate(self, data):
        from django.contrib.auth.models import User
        from .models import LoginRecord

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        try:
            login_record = LoginRecord.objects.get(
                user=user,
                ip_address=data['ip_address'],
                confirmed=False
            )
        except LoginRecord.DoesNotExist:
            raise serializers.ValidationError("Запись входа с таким IP не найдена")
        
        if not hasattr(login_record, 'confirmation_code'):
            raise serializers.ValidationError("В записи входа отсутствует код подтверждения")

        if login_record.confirmation_code != data['code']:
            raise serializers.ValidationError("Неверный код подтверждения")

        login_record.confirmed = True
        login_record.save()

        return data
