from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('confirm_email/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', views.log_out, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'), 
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit_username/', views.edit_username, name='edit_username'),
    path('profile/upload_photo/', views.upload_photo, name='upload_photo'),
    path('follow/', views.follow_user, name='follow_user'),
]
