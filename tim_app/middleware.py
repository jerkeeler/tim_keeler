from typing import Dict

from django.http import HttpRequest
from tim_keeler.settings import DEBUG


def debug_context_processor(request: HttpRequest) -> Dict:
    """This auto injects the DEBUG variable into every view context, making conditional rendering easier"""
    return {
        'DEBUG': DEBUG,
    }
