from django.db import models
from .manager import AccountManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'