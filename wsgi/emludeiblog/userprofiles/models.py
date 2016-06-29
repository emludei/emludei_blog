import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.template.loader import render_to_string

from .utils import create_activation_key


ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 7)


class User(AbstractUser):
    ACTIVATED = 'ACTIVATED'

    activation_key = models.CharField(
        verbose_name='activation key',
        max_length=100,
        default=ACTIVATED,
        editable=False
    )

    @classmethod
    def create_inactive_user(cls, username, password, email):
        new_user = cls(username=username, email=email, is_active=False)
        new_user.activation_key = create_activation_key(username)
        new_user.set_password(password)
        new_user.save()
        new_user.send_activation_email()

    @classmethod
    def delete_expired_profiles(cls):
        inactive_users = cls.objects.filter(is_active=False)
        [user.delete() for user in inactive_users if user.activation_key_expired()]

    def activate_user(self):
        self.is_active = True
        self.activation_key = self.ACTIVATED
        self.save()

    def activation_key_expired(self):
        expiration_date = datetime.timedelta(ACCOUNT_ACTIVATION_DAYS)
        return (self.activation_key == self.ACTIVATED or
                self.date_joined + expiration_date <= timezone.now())

    def send_activation_email(self):
        context = {
            'username': self.username,
            'activation_key': self.activation_key,
            'activation_days': ACCOUNT_ACTIVATION_DAYS
        }

        subject = render_to_string('userprofiles/activation_email_subject.txt')
        message = render_to_string('userprofiles/activation_email_message.txt', context)

        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
