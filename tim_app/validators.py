from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMinLength:
    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(f'Must be at least {self.min_length} characters long', params={'value': value})
