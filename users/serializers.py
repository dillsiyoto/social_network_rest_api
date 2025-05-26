from rest_framework import serializers
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "first_name", 
            "last_name", "email", "password"
        ]
        # exclude = ["password", "groups", "user_permissions"]


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=50
    )

#     def validate(self, attrs):
#         if len(attrs) < 8:
#             raise ValueError
#         return super().validate(attrs)


