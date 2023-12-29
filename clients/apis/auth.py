from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import UpdateAPIView

from clients.models import User
from clients.permissions import IsSystemAdmin
from clients.serializers import MyTokenObtainPairSerializer, ChangePasswordSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordApi(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return user
