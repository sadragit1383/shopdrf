"""
Models for the Custom User application.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """Manager for Custom User model with helper methods to create regular and superusers."""

    def create_user(self, mobile_number, password=None, **extra_fields):
        """
        Create and return a regular user with a mobile number and password.
        """
        if not mobile_number:
            raise ValueError("Users must have a mobile number")

        extra_fields.setdefault("is_active", False)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        Create and return a superuser with a mobile number and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(mobile_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses mobile number as the unique identifier."""

    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='ایمیل')
    name = models.CharField(max_length=60, blank=True, null=True, verbose_name='نام')
    family = models.CharField(max_length=60, blank=True, null=True, verbose_name='خانوادگی')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت فعال بودن')
    password = models.CharField(max_length=128, verbose_name='رمز عبور')
    active_code = models.CharField(max_length=16, blank=True, null=True, verbose_name='کد تایید')
    gender_choices = (('M', 'مرد'), ('F', 'زن'))
    gender = models.CharField(max_length=1, choices=gender_choices, default='M', verbose_name='جنسیت')
    is_admin = models.BooleanField(default=False, verbose_name='وضعیت ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'email', 'family']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.family} ({self.mobile_number})"

    @property
    def is_staff(self):
        """Check if the user is an admin (required for Django admin)."""
        return self.is_admin

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.name} {self.family}".strip()

    def get_short_name(self):
        """Return the short name (first name) of the user."""
        return self.name
