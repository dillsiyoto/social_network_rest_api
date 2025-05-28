from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "first_name", 
            "last_name", "email", "password"
        ]
        # exclude = ["password", "groups", "user_permissions"]

    def save(self, **kwargs):
        raw_password: str | None = kwargs.get("password")
        if raw_password:
            kwargs["password"] = make_password(password=raw_password)
        return super().save(**kwargs)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=50
    )

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=50)
    new_password = serializers.CharField(required=True, max_length=50)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("wrong password")
        return value
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password is too short")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()

#     def validate(self, attrs):
#         if len(attrs) < 8:
#             raise ValueError
#         return super().validate(attrs)


