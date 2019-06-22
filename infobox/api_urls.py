from rest_framework.routers import DefaultRouter
from infobox.viewsets import CategoryViewSet, InfoboxViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("infoboxes", InfoboxViewSet)


urlpatterns = router.urls
