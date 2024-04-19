from rest_framework.generics import CreateAPIView
from .serializers import CustomUserSerializer
from .models import CustomUser


class CustomUserCreate(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
