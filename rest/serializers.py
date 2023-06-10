from django.core import exceptions
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import User

import django.contrib.auth.password_validation as validators


class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        """
        Создание пользователя
        """
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        return user

    def validate(self, data):
        """
        Валидация пароля
        """
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ['id', 'avatar', 'sex', 'first_name',
                  'last_name', 'password', 'email']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}, }
