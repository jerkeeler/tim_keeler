from django.urls import path
from tim_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('calendar', views.calendar, name='calendar'),
    path('contact', views.contact, name='contact'),
    path('media', views.media, name='media'),
    path('healthcheck', views.healthcheck),
]
