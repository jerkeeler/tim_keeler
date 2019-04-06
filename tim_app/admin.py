from django.contrib import admin

from tim_app import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'ip', 'time_sent',)


@admin.register(models.Bio)
class BioAdmin(admin.ModelAdmin):
    pass
