from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r"^[\w.@+-]+\Z"
    flags = 0


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError('Год не может быть больше текущего')
