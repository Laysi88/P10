from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, age=None, can_be_contacted=None, can_data_be_shared=None):
        if not age:
            raise ValueError("L'âge de l'utilisateur doit être renseigné")
        if age < 15:
            raise ValueError("L'utilisateur doit avoir au moins 15 ans")
        if not username:
            raise ValueError("Vous devez renseigner un nom d'utilisateur")
        if len(username) < 4:
            raise ValueError("Le nom d'utilisateur doit comporter au moins 4 caractères")
        user = self.model(
            username=username, age=age, can_be_contacted=can_be_contacted, can_data_be_shared=can_data_be_shared
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, age):
        user = self.create_user(
            username=username,
            password=password,
            age=age,
            can_be_contacted=True,
            can_data_be_shared=True,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["age"]

    def __str__(self):
        return self.username
