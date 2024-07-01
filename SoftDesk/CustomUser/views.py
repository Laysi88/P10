from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CustomUserCreate(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserUpdate(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CustomUserDelete(DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({"details": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
