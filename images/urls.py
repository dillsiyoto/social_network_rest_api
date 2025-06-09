from rest_framework.routers import DefaultRouter
from .views import ImagesViewSet

router = DefaultRouter()
router.register(r'', ImagesViewSet, basename='images')

urlpatterns = router.urls