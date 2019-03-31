from django.core.mail import mail_admins
from django.db import models

from tim_app.validators import ValidateMinLength
from tim_app.consts import VARCHAR_LENGTH


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(TimeStampModel):
    time_sent = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    name = models.CharField(max_length=VARCHAR_LENGTH, validators=[ValidateMinLength(3)])
    email = models.EmailField(max_length=VARCHAR_LENGTH, null=True, blank=True)
    subject = models.CharField(max_length=VARCHAR_LENGTH, choices=[
        ('General Inquiry', 'General Inquiry'),
        ('Business', 'Business'),
        ('Misc.', 'Misc.'),
    ])
    message = models.TextField(validators=[ValidateMinLength(5)])

    def __str__(self):
        return self.name

    def deliver(self):
        mail_admins(
            f'[{self.subject}] from {self.name} on {self.time_sent.date()}',
            f'Subject: {self.subject}\n'
            f'Name: {self.name}\n'
            f'Email: {self.email}\n'
            f'Sent at: {self.time_sent}\n\n\n'
            f'{self.message}'
        )
