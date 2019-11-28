from django.urls import path
from supplication.views import NewSupplicationView, UpdateSupplicationView, NewSupplicationVariantView, \
    UpdateSupplicationVariantView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("infobox/<int:pk>/supplication/new", NewSupplicationView.as_view(), name="new"),
    path("infobox/<int:pk>/supplication/<int:supplication_id>/edit", UpdateSupplicationView.as_view(), name="edit"),
    path("infobox/<int:pk>/supplication/<int:supplication_id>/new", NewSupplicationVariantView.as_view(),
         name="new_variant"),
    path("infobox/<int:pk>/supplication/<int:supplication_id>/variant/<int:supplication_variant_id>/edit",
         UpdateSupplicationVariantView.as_view(),
         name="edit_variant"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
