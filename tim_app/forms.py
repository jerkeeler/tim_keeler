import logging

import requests
from django import forms
from django.http import HttpRequest

from tim_app.consts import RECAPTCHA_URL
from tim_app.models import Contact
from tim_keeler.settings import DEBUG, SETTINGS

logger = logging.getLogger(__name__)


def is_captcha_valid(request: HttpRequest) -> bool:
    if request.method != 'POST':
        logger.warning('Attempted to validate ReCaptcha on non-post request')
        return False

    recaptcha_response = request.POST.get('g-recaptcha-response')
    if recaptcha_response is None:
        return False or DEBUG

    verify_response = requests.post(RECAPTCHA_URL, data={
        'response': recaptcha_response,
        'secret': SETTINGS['captcha']['secret_key'],
        'remoteip': request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')),
    }).json()
    error_codes = verify_response.get('error_codes')
    if error_codes is not None:
        logger.warning(f'Recaptcha request failed with following error codes: {", ".join(error_codes)}')
    return verify_response['success'] or DEBUG


class ContactForm(forms.ModelForm):
    field_attrs = {
        'name': {
            'class': 'input',
            'placeholder': 'Jane Doe',
        },
        'email': {
            'class': 'input',
            'placeholder': 'janedoe@example.com',
        },
        'message': {
            'class': 'textarea',
            'placeholder': 'Hello, Tim!'
        }
    }

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update(self.field_attrs.get(visible.name, {}))
