from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **kwargs):
        if not login:
            raise ValueError("The Login field must be set")
        login = login.strip()
        user = self.model(login=login, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **kwargs):
        user = self.create_user(login, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=128, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)


    objects = UserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(f"Login: {self.login} | Registration date: {self.registration_date}")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"