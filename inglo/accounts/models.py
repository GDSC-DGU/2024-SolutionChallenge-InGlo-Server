from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(max_length=255, unique=True)
    name        = models.CharField(max_length=255, blank=True, null=True)
    profile_img = models.URLField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    country     = models.IntegerField(blank=True, null=True)
    language    = models.CharField(max_length=10, default="en")
    liked_total  = models.IntegerField(default=0)
    sketch_num   = models.IntegerField(default=0)
    feedback_total = models.IntegerField(default=0)
    additional_info_provided = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
