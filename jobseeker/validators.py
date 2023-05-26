from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_after_today(date):
    if timezone.now().date() > date:
        raise ValidationError(message=_('Tanggal tidak boleh sebelum hari ini'),code='invalid_date')
