from django.shortcuts import render
from django.http import HttpResponse

from .serializers import UserSerializer
from .models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
