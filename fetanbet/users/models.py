from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    username=None
    first_name=None
    last_name=None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
