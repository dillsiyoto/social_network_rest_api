from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from .models import Avatar, Images
from publics.models import Public
from .models import Gallery
from .serializers import GallerySerializer

class UpdateAvatarView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_file = request.FILES.get("image")
        target = request.data.get("target") 
        target_id = request.data.get("id")   

        if not image_file:
            return Response({"error": "No image file provided."}, status=400)

        with transaction.atomic():
            image = Images.objects.create(image=image_file)

            if target == "user":
                avatar, created = Avatar.objects.get_or_create(user=request.user)
                if avatar.images:
                    avatar.images.delete()
                avatar.images = image
                avatar.save()

            elif target == "public":
                try:
                    public = Public.objects.get(id=target_id)
                except Public.DoesNotExist:
                    return Response({"error": "Public not found"}, status=404)

                if public.owner != request.user:
                    return Response({"error": "Permission denied"}, status=403)
                
                avatar, created = Avatar.objects.get_or_create(public=public)
                if avatar.images:
                    avatar.images.delete()
                avatar.images = image
                avatar.save()

            else:
                return Response({"error": "Invalid target"}, status=400)

        return Response({"status": "Avatar has been updated."})

class AddToGalleryView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        images = request.FILES.getlist("images")
        target = request.data.get("target")
        target_id = request.data.get("id")   

        if not images:
            return Response({"error": "No images uploaded."}, status=400)

        if target == "user":
            gallery, created = Gallery.objects.get_or_create(user=request.user)
        elif target == "public":
            try:
                public = Public.objects.get(id=target_id)
            except Public.DoesNotExist:
                return Response({"error": "Public not found"}, status=404)
            
            if public.owner != request.user:
                    return Response({"error": "Permission denied"}, status=403)

            gallery, created = Gallery.objects.get_or_create(public=public)
        else:
            return Response({"error": "Invalid target."}, status=400)

        new_images = [Images(image=img) for img in images]
        created_images = Images.objects.bulk_create(new_images)
        gallery.images.add(*created_images)

        return Response({"status": f"{len(created_images)} images added to gallery."})


class PublicGalleryView(APIView):
    @method_decorator(cache_page(60 * 10))
    def get(self, request, public_id):
        try:
            gallery = (
                Gallery.objects
                .select_related("public")
                .prefetch_related("images")
                .get(public_id=public_id)
            )

        except Gallery.DoesNotExist:
            return Response({"error": "Gallery not found"}, status=404)

        return Response(GallerySerializer(gallery).data)