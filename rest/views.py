from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .serializers import UserSerializer, MatchRequestSerializer
from .models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class MatchRequestViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = MatchRequestSerializer

    def get_serializer_context(self):
        result = super().get_serializer_context()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        result['to_user'] = self.kwargs[lookup_url_kwarg]
        return result

    def send_match_email(self, user, addressee):
        rendered_msg = render_to_string(
            "rest/match_email_msg.html", {'name': user.first_name, 'email': user.email})
        send_mail(
            settings.MATCH_EMAIL_SUBJECT,
            rendered_msg,
            "info@diwos.ru",
            [addressee.email],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        new_match_request = get_object_or_404(
            User, id=self.kwargs[lookup_url_kwarg])
        if self.request.user.incoming_match_requests.filter(id=new_match_request.id).exists():
            with transaction.atomic():
                self.request.user.match.add(new_match_request)
                new_match_request.outgoing_match_requests.remove(
                    self.request.user)
            self.send_match_email(self.request.user, new_match_request)
            self.send_match_email(new_match_request, self.request.user)
            return {'email': new_match_request.email}
        else:
            self.request.user.outgoing_match_requests.add(new_match_request)
            return {}
