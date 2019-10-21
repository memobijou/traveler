from django.urls import path
from infobox.views import CategoryView, InfoboxView, InfoboxUpdateView, CategoryUpdateView, InfoboxDeleteView,\
    CategoryDeleteView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='new_category'),
    path('categories/<int:pk>/edit', CategoryUpdateView.as_view(), name='edit_category'),
    path("categories/<int:category_id>/infobox/new", InfoboxView.as_view(), name="new"),
    path("categories/<int:category_id>/infobox/<int:pk>/new", InfoboxView.as_view(), name="new"),
    path("categories/<int:category_id>/infobox/<int:pk>/edit", InfoboxUpdateView.as_view(), name="edit"),
    path("infobox/parent/<int:parent_id>/child/<int:pk>/edit", InfoboxUpdateView.as_view(), name="edit"),
    path("infobox/<int:pk>/edit", InfoboxUpdateView.as_view(), name="edit"),
    path("infobox/<int:pk>/new", InfoboxView.as_view(), name="new"),
    path("infobox/<int:pk>/delete", InfoboxDeleteView.as_view(), name="delete"),
    path("categories/delete/<int:parent_id>", CategoryDeleteView.as_view(), name="delete_category"),
    path("categories/delete", CategoryDeleteView.as_view(), name="delete_category")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
