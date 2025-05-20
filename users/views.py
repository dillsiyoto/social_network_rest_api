from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from users.serializators import UserModelSerializer


class UserViewSet(ViewSet):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserModelSerializer

    def list(self, request: Request) -> Response:
        serializer = UserModelSerializer(
            self.queryset, many=True
        )
        if not serializer.data:
            return Response(
                status=status.HTTP_404_NOT_FOUND, 
                data={"error": "users not found"}
            )
        return Response(
            data=serializer.data, 
            status=status.HTTP_200_OK
        )

    def create(
        self, request: Request
    ) -> Response:
        s = UserModelSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            User.objects.create(
                username=s.validated_data.get("username"),
                first_name=s.validated_data.get("first_name"),
                last_name=s.validated_data.get("last_name"),
                email=s.validated_data.get("email"),
                password=make_password(
                    s.validated_data.get("password")
            ))
            
            return Response(
                data={"message": "success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def retrieve(
        self, request: Request, pk=None
    ) -> Response:
        pass

    def update(
        self, request: Request, pk=None
    ) -> Response:
        pass

    def partial_update(
        self, request: Request, pk=None
    ) -> Response:
        pass

    def destroy(
        self, request: Request, pk=None
    ) -> Response:
        pass


