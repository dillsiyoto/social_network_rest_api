from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from users.serializers import UserModelSerializer, ChangePasswordSerializer


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        s = UserModelSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            User.objects.create(
                username=s.validated_data.get("username"),
                first_name=s.validated_data.get("first_name"),
                last_name=s.validated_data.get("last_name"),
                email=s.validated_data.get("email"),
                password=make_password(s.validated_data.get("password")),
            )

            return Response(
                data={"message": "success"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        if not serializer.data:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "users not found"},
            )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            data="Not implemented"
        )
        
    def get(self, request: Request, pk=None) -> Response:
        try:
            user = User.objects.get(pk=pk)
            serializer = UserModelSerializer(user)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(
                data={"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request: Request, pk=None) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user updated"})

    def patch(self, request: Request, pk=None) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user partial updated"})

    def delete(self, request: Request, pk=None) -> Response:
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            return Response(
                data={"message": "you have no power"},
                status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response(
            data={"message": "user has been deleted"}
        )


class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "password updated successfully"}, status=200)
    
    