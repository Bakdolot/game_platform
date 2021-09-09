from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(verbose_name=_('Телефон'),
                             max_length=12,
                             null=True, unique=True, validators=[
            RegexValidator(regex=r'^996\d{9}$',
                           message=_('Pass valid phone number'))
        ])
    otp = models.CharField(verbose_name=_('SMS code'), max_length=4)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.phone}->{self.username}-> {self.profile.get_region_display()}'


class 
