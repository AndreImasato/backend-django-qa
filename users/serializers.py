# pylint: disable=W0223
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserAccessLogs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        required=True,
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        required=True,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # Try to authenticate user using Django auth framework
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError(
                _("Access denied: wrong email and password"),
                code="no_active_account"
            )
        refresh = RefreshToken.for_user(user)
        pair_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return pair_token


class UserAccessLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessLogs
        exclude = ("access_timestamp",)
