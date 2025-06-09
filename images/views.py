from rest_framework import viewsets, permissions # импортируем вью, разрешения
from .models import Images # импортируем модель изображения
from .serializers import ImagesSerializer # импортируем созданный сериализатор
from rest_framework.permissions import IsAuthenticated # импортируем доступ для авторизованных

class ImagesViewSet(viewsets.ModelViewSet): # создаем вью для работы с изображениями
    permission_classes = [IsAuthenticated] # впускаем только авторизованных

    queryset = Images.objects.all() #берем все изображения из базы данных
    serializer_class = ImagesSerializer # сериализуем

    def perform_create(self, serializer): #создаем класс
        serializer.save(user=self.request.user) # сохраняем и присваиваем изображение текущему юзеру
