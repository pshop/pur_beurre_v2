from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from users.managers import CustomUserManager

from datetime import datetime
from datetime import timedelta
import uuid

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=150, default="Unknown")
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email

class ResetLink(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    link_id = models.CharField(max_length=150)
    expiration_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1), blank=True)

    def save(self):
        if not self.id:
            self.link_id = uuid.uuid4()
        super(ResetLink, self).save()
