from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


phone_validator = RegexValidator(regex=r'^996\d{9}$',
                           message=_('Pass valid phone number'))