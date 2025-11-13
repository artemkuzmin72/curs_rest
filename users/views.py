from rest_framework import generics
from .serializers import RegisterSerializer
from users.models import User
# Create your views here.


class RegisterView(generics.CreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
