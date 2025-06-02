from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from users.serializers import UserModelSerializer


class RegistrationViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request: Request) -> Response:
        raise MethodNotAllowed(method="list") # Можно вообще не писать этот метод

    def create(self, request: Request) -> Response:
        s = UserModelSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            User.objects.create_user(**s.validated_data)
            # User.objects.create(
            #     username=s.validated_data.get("username"),
            #     first_name=s.validated_data.get("first_name"),
            #     last_name=s.validated_data.get("last_name"),
            #     email=s.validated_data.get("email"),
            #     password=make_password(s.validated_data.get("password")),
            # )

            return Response(
                    data={"message": "User successfully registered"},
                    status=status.HTTP_201_CREATED # Лучше 201
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        # if not serializer.data:
        #     return Response(
        #         status=status.HTTP_404_NOT_FOUND,
        #         data={"error": "users not found"},
        #     ) # так делать не надо
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        raise MethodNotAllowed(method="create")
        
    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            user = User.objects.get(pk=pk)
            serializer = UserModelSerializer(user)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(
                data={"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request: Request, pk=None) -> Response:
        serializer = UserModelSerializer(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**serializer.validated_data)
        return Response(data={"message": "user updated"})

    def partial_update(self, request: Request, pk=None) -> Response:
        serializer = UserModelSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**serializer.validated_data)
        return Response(data={"message": "user partial updated"})

    def destroy(self, request: Request, pk=None) -> Response:
        user = get_object_or_404(User, pk=pk)
        # user: User | None = User.objects.filter(pk=pk).first()
        # if not user:
        #     return Response(
        #         data={"error": "user not found"},
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        if request.user.pk != user.pk:
            raise PermissionDenied(detail="you have no power here")
            # return Response(
            #     data={"message": "you have no power"},
            #     status=status.HTTP_403_FORBIDDEN # лушче 403
            # )
        user.delete()
        return Response(
            data={"message": "user has been deleted"}
        )
