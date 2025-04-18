from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import EmailSubscriptionForm
from .models import Subscriber


@require_POST
def subscribe(request):
    if request.user.is_authenticated:
        subscriber, created = Subscriber.objects.get_or_create(email=request.user.email)
        subscriber.is_subscribed = True
        subscriber.user = request.user
        subscriber.save()
        return JsonResponse({'status': 'ok'})
    else:
        form = EmailSubscriptionForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        subscriber.is_subscribed = True
        subscriber.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'form data not valid'})


@login_required
@require_POST
def unsubscribe(request):
    subscriber = request.user.subscription
    subscriber.is_subscribed = False
    subscriber.save()
    return JsonResponse({'status': 'ok', 'message': 'Вы успешно отписались'})

