from django.db import models
from django.utils.translation import gettext_lazy as _


class SendCodeType(models.IntegerChoices):
    REGISTER = 1, _('register')
    RESET_PASSWORD = 2, _('reset password')
    RESET_PHONE = 3, _('reset phone')