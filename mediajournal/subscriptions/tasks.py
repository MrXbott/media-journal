from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta

from .models import Subscriber
from articles.models import Article  


@shared_task
def send_weekly_newsletter():
    """
    Асинхронная Celery-задача для отправки еженедельной email-рассылки.

    Собирает все статьи, опубликованные за последнюю неделю, и отправляет 
    HTML-письмо подписанным пользователям. Шаблон письма — 'weekly_newsletter.html'.
    
    Получатели выбираются из модели Subscriber, где is_subscribed=True.
    Для генерации ссылок в шаблоне используется переменная settings.DOMAIN_URL.
    Тема письма берётся из settings.WEEKLY_NEWSLETTER_SUBJECT.
    """
    one_week_ago = timezone.now() - timedelta(days=7)
    new_articles = Article.objects.filter(published__gte=one_week_ago)

    html_content = render_to_string('weekly_newsletter.html', 
                                    {
                                        'articles': new_articles,
                                        'domain': settings.DOMAIN_URL,
                                    })

    recipients = Subscriber.objects.filter(is_subscribed=True).values_list('email', flat=True)
    
    for email in recipients:
        email_message = EmailMultiAlternatives(settings.WEEKLY_NEWSLETTER_SUBJECT, 
                                               html_content, 
                                               settings.DEFAULT_FROM_EMAIL, 
                                               [email])
        email_message.send()
