from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.utils import Utils

from .models import AccessTypes, UserAccessLogs
from .serializers import LoginSerializer, UserAccessLogsSerializer


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
                user = authenticate(
                    request,
                    email=request.data.get('email'),
                    password=request.data.get('password')
                )
                user_access_log_data = {
                    "user": user,
                    "access_type": AccessTypes.EMAIL_PASSWORD,
                    "user_agent": user_agent,
                    "platform": platform,
                    "ip_address": ip_address,
                }

                access_log_data = UserAccessLogsSerializer(
                    data=user_access_log_data
                )
                #TODO checks why is not valid
                if access_log_data.is_valid():
                    print("CRIANDOOOO")
                    access_log_data.save()
            return response
        except InvalidToken as e:
            raise e
