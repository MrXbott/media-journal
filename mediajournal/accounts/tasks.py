from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives


@shared_task
def send_confirm_email(subject: str, message: str, to_email: str):
    '''This function sends confirmation email (as a background task) after user registration'''
    email = EmailMessage(subject, message, to=[to_email]) 
    email.send() 


@shared_task
def send_password_reset_email(subject, body, from_email, to_email):
    email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    email_message.send()