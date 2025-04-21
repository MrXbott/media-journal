from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives


@shared_task
def send_confirm_email(subject: str, message: str, to_email: str):
    """
    Отправляет письмо с подтверждением регистрации пользователю.

    Используется при регистрации нового пользователя для отправки письма с
    активационной ссылкой на email.

    Аргументы:
        subject (str): Тема письма.
        message (str): Текст письма в формате HTML или Plain.
        to_email (str): Email-адрес получателя.
    """
    email = EmailMessage(subject, message, to=[to_email]) 
    email.send() 


@shared_task
def send_password_reset_email(subject: str, body: str, from_email: str, to_email: str):
    """
    Отправляет письмо для сброса пароля.

    Используется при восстановлении пароля через email.

    Аргументы:
        subject (str): Тема письма.
        body (str): Тело письма.
        from_email (str): Email отправителя.
        to_email (list): Список email-адресов получателей.
    """
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    email_message.send()