from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .manager import UserManager


class CustomUser(AbstractUser):

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits"
    )

    username = None
    phone_number = models.CharField(
        validators=[phone_validator],
        max_length=10,
        unique=True
    )
    full_name = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def __str__(self):
        return self.phone_number