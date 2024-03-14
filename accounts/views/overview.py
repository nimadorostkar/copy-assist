from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User

class OverView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user=self.request.user
        data = {
            "user": self.serializer_class(user).data,
            "ticket_count": None, #Invoice.objects.filter(user=user,status="پرداخت نشده").count(),
            "tickets": None, #InvoiceSerializer(Invoice.objects.filter(user=user,status="پرداخت نشده"),many=True).data,
            "none": None,
            "none": None,
        }

        return Response(data, status=status.HTTP_200_OK)