from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, pre_init, post_init, pre_migrate, post_migrate
from django.core.signals import request_started, request_finished, got_request_exception
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Student
import logging


logger = logging.getLogger(__name__)

""" Model signals"""

@receiver(pre_save, sender=Student)
def before_student_save(sender, instance, **kwargs):
    print(f"Before saving Student: {instance.name}")

@receiver(post_save, sender=Student)
def after_student_save(sender, instance, created, **kwargs):
    if created:
        print(f"New Student created: {instance.name}")
    else:
        print(f"Student updated: {instance.name}")

@receiver(pre_delete, sender=Student)
def before_student_delete(sender, instance, **kwargs):
    print(f"Before deleting Student: {instance.name}")

@receiver(post_delete, sender=Student)
def after_student_delete(sender, instance, **kwargs):
    print(f"Deleted Student: {instance.name}")






""" Request signals """

# 1. When request starts
@receiver(request_started)
def at_request_start(sender, **kwargs):
    print(" Request Started... A visitor came to the website!")

# 2. When request finishes
@receiver(request_finished)
def at_request_finish(sender, **kwargs):
    print(" Request Finished... Response sent to the browser!")

# 3. When exception occurs during request
@receiver(got_request_exception)
def at_request_exception(sender, **kwargs):
    exception = kwargs.get('exception')
    print('exception', exception)

    if exception:
        print(f" Oops! An exception occurred: {exception}")  
        logger.error(f"An exception occurred: {exception}")






""" Authentication signals """

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    This function is triggered when a user successfully logs in.
    """
    login_time = now()
    logger.info(f"User {user.username} logged in at {login_time}")

    # Optionally, you can update the last login time in the database
   
    # user.profile.last_login_time = login_time
    # user.profile.save()

    # You can also print it to the console
    print(f"User {user.username} logged in at {login_time}")




@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """
    This function is triggered when a user logs out.
    We log the user's logout event.
    """
    logger.info(f"User {user.username} logged out.")

    # Optionally, you can perform other actions here, like updating the user status
    print(f"User {user.username} logged out.")



@receiver(user_login_failed)
def user_login_failed_handler(sender, credentials, request, **kwargs):
    """
    This function is triggered when a login attempt fails.
    We log the failed login attempt and credentials (e.g., username).
    """
    username = credentials.get('username', 'Unknown')
    logger.warning(f"Failed login attempt for username: {username}")

    # Optionally, you can add actions such as blocking the account after failed attempts
    print(f"Failed login attempt for username: {username}")







""" Migrations """

# This runs BEFORE migrations are applied
@receiver(pre_migrate)
def before_migrations(sender, **kwargs):
    print(" pre_migrate: Migrations are about to start!")
    logger.info("Migrations are about to start...")

# This runs AFTER migrations are applied
@receiver(post_migrate)
def after_migrations(sender, **kwargs):
    print(" post_migrate: Migrations have finished!")
    logger.info("Migrations finished successfully!")





"""Management commands"""

# 1. Before a Student instance is created
@receiver(pre_init, sender=Student)
def before_student_created(sender, *args, **kwargs):
    print(" [pre_init] About to create a Student instance!")

    # Get the 'name' field from kwargs
    name = kwargs.get('name', None)

    if name:
        print(f"Incoming Student Name: {name}")
    else:
        print("No student name provided!")


# 2. After a Student instance is created
@receiver(post_init, sender=Student)
def after_student_created(sender, instance, **kwargs):
    print(" [post_init] Student instance created!")
    print(f"Student Name: {instance.name} | Marks: {instance.marks}")








