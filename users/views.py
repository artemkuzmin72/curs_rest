from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
# Create your views here.


class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
