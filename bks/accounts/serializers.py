from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user

    def validate_password(self, value):
        validate_password(value)
        return value


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'nickname',)
        read_only_fields = ('pk','email')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['email'] = instance.email
        ret['nickname'] = instance.nickname
        return ret