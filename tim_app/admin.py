from django.contrib import admin

from tim_app.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'ip', 'time_sent',)
