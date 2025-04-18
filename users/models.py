
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.update({'is_staff': True, 'is_superuser': True, 'role': 1})
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLES = ((1, 'Admin'), (2, 'Host'), (3, 'Passenger'))
    role = models.IntegerField(choices=ROLES, default=3)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role_change_requested = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
