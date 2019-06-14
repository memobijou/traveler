from django.urls import path
from infobox.views import CategoryView

urlpatterns = [
    path('', CategoryView.as_view(), name='category'),
    path('<int:pk>/', CategoryView.as_view(), name='new_category'),
]
