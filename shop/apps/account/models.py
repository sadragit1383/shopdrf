"""
Models for the Custom User application.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """Manager for Custom User model."""

    def create_user(self, mobile_number, password=None, **extra_fields):
        """
        Create and return a normal user with an email and password.
        """
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(mobile_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model."""

    mobile_number = models.CharField(max_length=11, verbose_name='شماره موبایل', unique=True)
    email = models.EmailField(max_length=100, verbose_name='ایمیل', blank=True, null=True)
    name = models.CharField(max_length=60, verbose_name='نام', blank=True, null=True)
    family = models.CharField(max_length=60, verbose_name='خانوادگی', blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='وضعیت', blank=True, null=True)
    password = models.CharField(max_length=100, verbose_name='رمز عبور', blank=True, null=True)
    active_code = models.CharField(max_length=16, verbose_name='کد تایید', blank=True, null=True)
    GENDER_LIST = (('True', 'مرد'), ('False', 'زن'))
    gender = models.CharField(max_length=10, choices=GENDER_LIST, default='True')
    is_admin = models.BooleanField(default=False, verbose_name='وضعیت ادمین')

    objects = CustomUserManager()
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'email', 'family']

    @property
    def is_staff(self):
        """Return True if the user is an admin."""
        return self.is_admin