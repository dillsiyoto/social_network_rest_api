from rest_framework import serializers
from images.models import Gallery, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["id", "image", "created_at"]

class GallerySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Gallery
        fields = ["id", "images"]
