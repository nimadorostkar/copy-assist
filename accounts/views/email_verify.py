from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses
from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.serializers import UserSerializer, UserRegisterSerializer
from accounts.models import User



class EmailVeriy(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id", "")
        otp_code = self.request.data.get("otp_code", "")
        try:
            user_id = OneTimePassword.verify_otp(otp_id, otp_code)
        except ValueError:
            return Response(
                {"success": False, "errors": [_("OTP is invalid")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user(id=user_id) # self.request.user #

        access, refresh = login(user)

        data = {
            "refresh_token": refresh,
            "access_token": access,
            "user_data": UserSerializer(user).data,
        }
        response = Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
        #print('----------------------access-----')
        #print(access)
        #print('---------------------------------')
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response

