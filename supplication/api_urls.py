from rest_framework.routers import DefaultRouter
from supplication.viewsets import SupplicationViewSet

router = DefaultRouter()
# router.register("categories", CategoryViewSet, basename="category")
# router.register("infoboxes", InfoboxViewSet)


urlpatterns = router.urls
