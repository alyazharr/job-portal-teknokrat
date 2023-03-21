from ..validators import validate_after_today
from django.test import TestCase
from datetime import  timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

class ValidatorsTestCase(TestCase):

    def test_validate_after_today_if_date_is_before_today_should_raise_error(self):
        self.assertRaises(
            ValidationError,
            validate_after_today,
            timezone.now().date() - timedelta(days=1)
            )

    def test_validate_after_today_if_today_should_not_throw_error(self):
        try:
            validate_after_today(timezone.now().date())

        except Exception :
            self.fail()
    
    def test_validate_after_today_if_after_today_should_not_throw_error(self):
        try:
            validate_after_today(timezone.now().date() + timedelta(days=1))
        except Exception :
            self.fail()