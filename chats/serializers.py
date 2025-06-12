from rest_framework import serializers

from chats.models import Chat, Message
from users.serializers import UserSerializer

#
# class UserChatSerializer(serializers.Serializer):
#     id = serializers.IntegerField()

class ChatViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = UserSerializer(many=True)

class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data: dict):
        chat = Chat(
            is_group=validated_data.get("is_group"),
            title=validated_data.get("title"),
        )
        chat.save()
        users = validated_data.get("users")
        chat.users.set(users)
        return chat

    def update(self, instance: Chat, validated_data: dict):
        users = validated_data.pop("users")
        if users:
            instance.users.set(users)
        return super().update(instance, validated_data)
