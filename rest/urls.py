from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('clients/create',
         views.UserView.as_view(), name="create"),
    path('clients/auth/', include('rest_framework.urls')),
    path('clients/<int:pk>/match',
         views.MatchRequestView.as_view(), name="match"),
    path('list', views.UserListView.as_view(), name="users_list"),
]
