from __future__ import unicode_literals
import logging
from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, Group
from django.contrib.auth.base_user import AbstractBaseUser
from django.template.loader import render_to_string

from .managers import UserManager
from .utils.mail import *


# Create your models here.

class TimedStampModel(models.Model):
    """
    An abstract base class model that provides
    self-updating ``created_at`` and ``updated_at`` fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(models.Model):
    """
    An abstract base class model that provides
    self-updating ``created_at`` and ``updated_at`` fields
    """

    job = models.CharField(max_length=100, blank=True, null=True)
    job_position = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True)


class User(AbstractBaseUser, PermissionsMixin, TimedStampModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, null=True)
    password_reset_token = models.CharField(max_length=255, null=True)
    profile = models.OneToOneField(UserProfile, blank=True, null=True, related_name='profile', on_delete=models.PROTECT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email']

    objects = UserManager()

    def __str__(self):
        return f'<User {self.email} />'

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def send_activation_email(self):
        import urllib.error
        logging.info('Begin sending account activation email')
        # Render template with token
        email_str = render_to_string(
            'core/mail/activate_account.html',
            {'token_link': make_account_token_link(self.activation_token)}
        )
        # Send activation email
        try:
            send_mail(
                from_email=settings.ADMIN_EMAIL,
                subject='[TEA] Kích hoạt tài khoản',
                to_email=self.email,
                content=email_str
            )
        except urllib.error.HTTPError as e:
            logging.error(e)
        logging.info('Finish sending account activation email')

    def activate(self):
        self.is_active = True
        self.activation_token = None
        self.save()
        return self

    @staticmethod
    def generate_password_reset_token():
        import uuid
        return uuid.uuid4().hex[:25]

    def send_password_reset_email(self):
        import urllib.error
        # Set password reset token for user
        self.password_reset_token = User.generate_password_reset_token()
        self.save()
        logging.info(f'password reset token: {self.password_reset_token}')
        # Render template with token
        email_str = render_to_string(
            'core/mail/password_reset.html',
            {'token_link': make_password_reset_link(self.password_reset_token)}
        )
        # Send activation email
        try:
            send_mail(
                from_email=settings.ADMIN_EMAIL,
                subject='[SANV] Khôi phục mật khẩu',
                to_email=self.email,
                content=email_str
            )
        except urllib.error.HTTPError as e:
            logging.error(e)

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.password_reset_token = None
        self.save()

        return self
