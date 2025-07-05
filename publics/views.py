from django.shortcuts import render

# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema

from publics.models import Public, PublicInvite
from publics.serializers import (
    PublicSerializer, 
    PublicViewSerializer,
    PublicInviteSerializer
)


class PublicViewSet(ViewSet):
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(timeout=60*10))
    def list(self, request: Request) -> Response:
        publics: QuerySet[Public] = Public.objects.select_related(
            "owner"
        ).prefetch_related("members").filter(is_private=False)
        serializer = PublicViewSerializer(
            instance=publics, many=True
        )
        return Response(data=serializer.data)

    @method_decorator(cache_page(timeout=600))
    def retrieve(self, request: Request, pk: int) -> Response:
        # public: Public = get_object_or_404(
        #     Public, pk=pk, members=request.user
        # )
        public = Public.objects.select_related("owner").get(pk=pk)
        serializer = PublicViewSerializer(instance=public)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        request_body=PublicSerializer,
        responses={
            200: PublicViewSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request: Request) -> Response:
        serializer = PublicSerializer(
            data=request.data,
            context={"owner": request.user}
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        response_serializer = PublicViewSerializer(instance=obj)
        return Response(data=response_serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        pass

    def partial_update(self, request: Request, pk: int) -> Response:
        pass

    def destroy(self, request: Request, pk: int) -> Response:
        pass


class PublicInviteViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        invites = PublicInvite.objects.filter(invited_user=request.user)
        serializer = PublicInviteSerializer(invites, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        public_id = request.data.get("public")
        invited_user_id = request.data.get("invited_user")

        if not public_id or not invited_user_id:
            return Response(
                {"detail": "Нужны public и invited_user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        public = get_object_or_404(Public, id=public_id)

        if request.user != public.owner and request.user not in public.members.all():
            raise PermissionDenied("Вы не можете приглашать в этот паблик")

        invited_user = get_object_or_404(User, id=invited_user_id)

        invite, created = PublicInvite.objects.get_or_create(
            public=public,
            invited_user=invited_user,
            defaults={"invited_by": request.user}
        )

        serializer = PublicInviteSerializer(instance=invite)
        return Response(serializer.data, status=(
            status.HTTP_201_CREATED if created else status.HTTP_200_OK
        ))

    def update(self, request: Request, pk=None) -> Response:
        invite = get_object_or_404(PublicInvite, pk=pk, invited_user=request.user)
        invite.accepted = True
        invite.public.members.add(request.user)
        invite.save()
        return Response({"detail": "Приглашение принято"})
