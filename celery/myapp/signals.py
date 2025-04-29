# students/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from .tasks import schedule_email_tasks

@receiver(post_save, sender=Student)
def send_welcome_emails(sender, instance, created, **kwargs):
    if created:
        print('---------------------------')
        print('created')
        print('---------------------------')
        schedule_email_tasks.delay(instance.id)
