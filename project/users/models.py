from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    is_cashier = models.BooleanField(verbose_name='is cashier')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_cashier']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
