from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView, LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from .forms import RegistrationForm, UserPhotoEditForm, ProfileEditForm
from .token import email_verification_token
from .tasks import send_confirm_email
from .models import User
from articles.models import Article, Category


def registration(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            current_site = get_current_site(request) 
            subject = settings.CONFIRM_EMAIL_SUBJECT
            message = render_to_string('registration/confirm_email.html', { 
                'user': user, 
                'protocol': 'http:',
                'domain': current_site.domain, 
                'uid': urlsafe_base64_encode(force_bytes(user.id)), 
                'token': email_verification_token.make_token(user), 
            }) 
            to_email = form.cleaned_data.get('email') 
            send_confirm_email.delay(subject, message, to_email)
            return render(request, 'registration/email_confirmation.html', {'user': user})  
        else:
            messages.error(request, 'При создании аккаунта возникла ошибка')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


def confirm_email(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    '''Validates the activation link from a confirmation email.'''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/registration_done.html')
    return render(request, 'registration/activation_error.html')

# @login_required
# def log_out(request):
#     url = reverse('login') if isinstance(request.user, User) else reverse('admin:index')
#     logout(request)
#     return redirect(url)


def profile(request, id):
    user = get_object_or_404(User, id=id)
    categories = Category.objects.filter(parent=None).order_by('name')
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    return render(request, 'account/profile.html', {'user': user, 
                                                    'last_articles': last_articles,
                                                    'categories': categories,
                                                    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form': form})

@login_required
def edit_username(request):
    new_username = request.POST.dict()['username']
    user = User.objects.get(id=request.user.id)
    
    if User.objects.filter(username=new_username) and User.objects.filter(username=new_username).first() != user:
        return JsonResponse({'message': 'This username already taken'})
    
    if new_username and new_username != user.username:
        user.username = new_username
        user.save()
        return JsonResponse({'message': 'Your username updated successfully'})
    return JsonResponse({'message': 'You already have this username'})



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user
    





