from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager (BaseUserManager):
    def create_user (self, email, username, first_name, last_name, password=None):
        if not email or not username or not first_name or not last_name:
            raise ValueError ("User must have email, username, first name and last name")
        
        user = self.model (
            email = self.normalize_email (email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        
        user.set_password (password)
        user.save (using=self._db)

        return user
    
    def create_superuser (self, email, username, first_name, last_name, password):
        user = self.create_user (
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.save (using=self._db)

        return user

class Account (AbstractBaseUser):
    first_name = models.CharField (max_length=32)
    last_name = models.CharField (max_length=32)
    username = models.CharField (max_length=32, unique=True)
    email = models.EmailField (unique=True)
    phone = models.CharField (max_length=16, blank=True)

    # required fields
    date_joined = models.DateTimeField (auto_now_add=True)
    last_login = models.DateTimeField (auto_now=True)

    is_admin = models.BooleanField (default=False)
    is_staff = models.BooleanField (default=False)
    is_active = models.BooleanField (default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name"
    ]

    objects = AccountManager ()

    def __str__ (self):
        return self.email
    
    def has_perm (self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms (self, app_label):
        return True