from rest_framework import serializers

from publics.models import Public, PublicInvite
from users.serializers import UserSerializer


class PublicSerializer(serializers.Serializer):
    owner = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=200)
    is_private = serializers.BooleanField(default=False)
    members = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate(self, attrs: dict):
        title = attrs.get("title")
        if Public.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                detail=f"Public with title: {title} already exist!"
            )
        return super().validate(attrs)

    def create(self, validated_data: dict):
        public = Public(
            owner=validated_data.get("owner"),
            title=validated_data.get("title"),
            is_group=validated_data.get("is_group")
        )
        public.save()
        public.members.set(objs=validated_data.get("members"))
        return public
    
    def update(self, instance: Public, validated_data: dict):
        return super().update(instance, validated_data)


class PublicInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicInvite
        fields = "__all__"
        read_only_fields = ("invited_by", "created_at", "accepted")