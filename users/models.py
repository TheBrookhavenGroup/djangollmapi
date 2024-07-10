from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager


class Member(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    #    first_name = models.CharField(max_length=30, blank=True)
    #    last_name = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        ordering = ['email']

    def __str__(self):
        return self.email
