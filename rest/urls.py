from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('clients/create',
         views.UserViewSet.as_view({'post': 'create'}), name="create"),
    path('clients/auth/', include('rest_framework.urls')),
]
