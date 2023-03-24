from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.utils import Utils

from .models import AccessTypes
from .serializers import (LoginSerializer, UserAccessLogsSerializer,
                          UserSerializer)

User = get_user_model()


# Create your views here.
class LoginView(TokenObtainPairView):
    __doc__ = "View containing login with email and password option"
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Endpoint to get JWT pair token (access and refresh tokens)"
    )
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                user_agent, platform, ip_address = Utils.get_request_info(
                    request
                )
                user = User.objects.filter(email=request.data.get('email'))\
                    .first()
                user_access_log_data = {
                    "user": user.id,
                    "access_type": AccessTypes.EMAIL_PASSWORD,
                    "user_agent": user_agent,
                    "platform": platform,
                    "ip_address": ip_address,
                }

                access_log_data = UserAccessLogsSerializer(
                    data=user_access_log_data
                )
                if access_log_data.is_valid():
                    access_log_data.save()
                else:
                    return Response(
                        access_log_data.errors,
                        status.HTTP_400_BAD_REQUEST
                    )
            return response
        except InvalidToken as e:
            raise e


class LoginWithTokenView(APIView):
    __doc__ = 'View containing login with token option'
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Endpoint to login with JWT access token"
    )
    def post(self, request):
        user_agent, platform, ip_address = Utils.get_request_info(
            request
        )
        user = request.user
        data = {
            "user": user.id,
            "access_type": AccessTypes.ACCESS_TOKEN,
            "user_agent": user_agent,
            "platform": platform,
            "ip_addres": ip_address
        }
        access_log_data = UserAccessLogsSerializer(
            data=data
        )
        if access_log_data.is_valid():
            access_log_data.save()
            return Response("OK", status=status.HTTP_200_OK)
        return Response(
            access_log_data.errors,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema_view(
    list=extend_schema(
        description="Lists all users"
    ),
    create=extend_schema(
        description="Creates new user"
    ),
    retrieve=extend_schema(
        description="Fetches user details"
    ),
    partial_update=extend_schema(
        description="Updates user details"
    ),
    delete_user=extend_schema(
        description='"Deletes" user (deactivates him/her)'
    ),
    reactivate_user=extend_schema(
        description='Reactivates user'
    )
)
class UserView(ModelViewSet):   # pylint: disable=R0901
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    # Changes default lookup field for details endpoints
    lookup_field = 'public_id'

    @action(
        detail=True,
        methods=['delete'],
        url_path=r'delete-user',
        permission_classes=[IsAdminUser]
    )
    def delete_user(self, request, public_id=None):  # pylint: disable=W0613
        user = self.get_object()
        user.deactivate()
        return Response(
            {"user": user.public_id},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=['patch'],
        url_path=r'reactivate-user',
        permission_classes=[IsAdminUser]
    )
    def reactivate_user(
        self, request, public_id=None
    ):  # pylint: disable=W0613
        user = self.get_object()
        user.activate()
        return Response(
            {"user": user.public_id}
        )
