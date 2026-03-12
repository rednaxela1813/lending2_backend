from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from apps.company.models import CompanyInfo


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ManagerProfile(models.Model):
    ROLE_CHOICES = [("manager", "Content Manager"), ("admin", "Company Admin")]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="manager_profile"
    )
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name="managers")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="manager")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("company", "user_id")

    def __str__(self):
        return f"{self.user.email} ({self.company.name})"

    @property
    def is_admin(self):
        return self.role == "admin"
