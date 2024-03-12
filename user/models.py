from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Validators for the Users class fields:
password_validator = RegexValidator(
    regex=r'^.{8,}$',
    message='The password must have at least 8 characters.'
)

email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    message='Please enter a valid email'
)


class Users(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='profile')  # noqa
    first_name = models.CharField(
        'First Name', max_length=30, null=False, blank=False,)
    last_name = models.CharField(
        'Last Name', max_length=30, null=False, blank=False,)
    username = models.CharField('Username', null=False, blank=False, max_length=30,  # noqa
                                unique=True,)  # noqa
    email = models.EmailField('E-mail', validators=[
                              email_validator], null=False, blank=False,
                              unique=True,)

    password = models.CharField('Password', max_length=128, validators=[  # noqa
                                password_validator], null=False, blank=False,)  # noqa
    password_confirmation = models.CharField(
        'Password Confirmation', max_length=128, null=False, blank=False,)  # noqa
