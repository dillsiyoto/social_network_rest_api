from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import (
    MethodNotAllowed, PermissionDenied
)
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
            return Response(
                    data={"message": "User successfully registered"},
                    status=status.HTTP_201_CREATED # Лучше 201
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_user(request: Request, pk: int) -> User:
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied(detail="you have no power here")
        return user

    def list(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    def create(self, request: Request) -> Response:
        raise MethodNotAllowed(method="create")
        
    def retrieve(self, request: Request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(user)
        return Response(data=serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        user = self.check_user(request=request, pk=pk)
        serializer = UserModelSerializer(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user updated"})

    def partial_update(self, request: Request, pk: int) -> Response:
        user = self.check_user(request=request, pk=pk)
        serializer = UserModelSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user partial updated"})

    def destroy(self, request: Request, pk: int) -> Response:
        user = self.check_user(request=request, pk=pk)
        user.delete()
        return Response(
            data={"message": "user has been deleted"}
        )
