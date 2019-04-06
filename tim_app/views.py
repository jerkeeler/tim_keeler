import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from tim_app.forms import ContactForm, is_captcha_valid
from tim_app.models import Bio
from tim_keeler.settings import SETTINGS

logger = logging.getLogger(__name__)


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'tim_app/home.html')


@require_GET
def about(request: HttpRequest) -> HttpResponse:
    bio = Bio.objects.filter(active=True).first()
    if bio is None:
        paragraphs = []
    else:
        paragraphs = [p.strip() for p in bio.bio.split('\n') if p.strip()]
    return render(request, 'tim_app/about.html', {'bio': paragraphs})


@require_GET
def calendar(request: HttpRequest) -> HttpResponse:
    return render(request, 'tim_app/calendar.html')


@require_GET
def media(request: HttpRequest) -> HttpResponse:
    return render(request, 'tim_app/media.html')


@require_http_methods(['GET', 'POST'])
def contact(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        captcha_valid = is_captcha_valid(request)
        if captcha_valid and form.is_valid():
            contact_model = form.save(commit=False)
            contact_model.ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            contact_model.save()
            contact_model.deliver()
            return render(request, 'tim_app/thanks.html')
        elif not captcha_valid:
            return render(request, 'tim_app/thanks.html')
    else:
        form = ContactForm()
    return render(request, 'tim_app/contact.html', {'form': form, 'site_key': SETTINGS['captcha']['site_key']})
