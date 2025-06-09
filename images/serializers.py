from rest_framework import serializers # импортируем сериализаторв
from .models import Images # импортируем модель изображения

class ImagesSerializer(serializers.ModelSerializer): # создаем класс
    class Meta: # 
        model = Images # используем модель изображений от джанго
        fields = ['id', 'image', 'user'] # поля, которые будут сериализоваться
        read_only_fields = ['id', 'user'] # айди и юзер можем только читать
