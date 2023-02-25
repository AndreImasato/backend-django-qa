import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), unique=True, max_length=50)
    public_id = models.CharField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=36
    )
    address = models.CharField(
        _("user address"),
        blank=True,
        null=True,
        max_length=255
    )
    phone_number = models.CharField(
        _("user phone number"),
        blank=True,
        null=True,
        max_length=30
    )
    user_document = models.CharField(
        _("user document"),
        blank=True,
        null=True,
        max_length=50
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def activate(self) -> None:
        """
        Method to activate user
        """
        self.is_active = True
        self.save()

    def deactivate(self) -> None:
        """
        Method to deactivate user
        """
        self.is_active = False
        self.save()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")

    def __str__(self):
        return self.email
