# students/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta

@shared_task
def send_email_task(email, subject, message):
    send_mail(
        subject,
        message,
        'from@example.com',
        [email],
        fail_silently=False,
    )

@shared_task
def schedule_email_tasks(student_id):
    from .models import Student
    student = Student.objects.get(id=student_id)
    print('--------------------------')
    print('student',student)

    # Send first email after 5 minutes
    send_email_task.apply_async((student.email, 'Welcome!', 'Your first email.'), countdown=300)

    # Send second email 1 hour after the first one
    send_email_task.apply_async((student.email, 'Second Email', 'Your second email.'), countdown=3600)

    # Send third email 1 hour after the second one
    send_email_task.apply_async((student.email, 'Third Email', 'Your third email.'), countdown=7200)
