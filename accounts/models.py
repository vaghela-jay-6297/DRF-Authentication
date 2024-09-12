from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# user manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, role):
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role):
        user = self.create_user(username, email, password, role)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


# Customized User Model
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('employee', 'Employee'),
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def is_new(self):
        """ return true when create or update new user from django admin panel """
        return self._state.adding

