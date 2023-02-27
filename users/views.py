from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from common.utils import Utils

from .models import AccessTypes
from .serializers import (LoginSerializer, UserAccessLogsSerializer,
                          UserSerializer)


User = get_user_model()


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

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
                #TODO else return bad request
            return response
        except InvalidToken as e:
            #TODO return response
            raise e


#TODO create user view
class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    #TODO override retrieve (by public_id)
    #TODO override update (by public_id)
    #TODO override destroy (by public_id)
