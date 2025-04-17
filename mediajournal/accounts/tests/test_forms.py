from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from unittest.mock import patch
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django import forms

from accounts.models import User
from accounts.forms import RegistrationForm, CustomPasswordResetForm
from accounts.tasks import send_password_reset_email


class RegistrationFormTests(TestCase):
    def test_form_valid_data_creates_user(self):
        """
        Форма создаёт пользователя при корректных данных
        """
        form_data = {
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, form_data['email'])
        self.assertTrue(user.check_password(form_data['password1']))

    def test_form_passwords_do_not_match(self):
        """
        Форма не валидна, если пароли не совпадают
        """
        form_data = {
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'WrongPassword456!',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['Пароли не совпадают'])

    def test_form_invalid_password(self):
        """
        Форма не валидна, если пароль не проходит валидацию (например, слишком короткий)
        """
        form_data = {
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_form_missing_fields(self):
        """
        Форма не валидна, если отсутствуют обязательные поля
        """
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_user_not_saved_if_commit_false(self):
        """
        Пользователь не сохраняется в базу, если commit=False
        """
        form_data = {
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        self.assertIsNone(user.id)


class CustomPasswordResetFormTests(TestCase):
    def setUp(self):
        """
        Создаёт тестового активного пользователя и фабрику запросов.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create(
            email='user@example.com',
            username = 'user',
            is_active=True
        )
        self.user.set_password('Password123!')
        self.user.save()

    def test_form_valid_with_existing_user(self):
        """
        Проверяет, что форма валидна при вводе существующего email.
        """
        form = CustomPasswordResetForm(data={'email': 'user@example.com'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_unknown_email(self):
        """
        Проверяет, что форма валидна даже при несуществующем email, но метод get_user возвращает None.
        """
        form = CustomPasswordResetForm(data={'email': 'unknown@example.com'})
        self.assertTrue(form.is_valid())  # форма не должна падать при несуществующем email
        user = form.get_user('unknown@example.com')
        self.assertIsNone(user)

    def test_get_user_returns_active_user(self):
        """
        Проверяет, что get_user возвращает активного пользователя по email.
        """
        form = CustomPasswordResetForm()
        user = form.get_user('user@example.com')
        self.assertEqual(user, self.user)

    @patch('accounts.forms.send_password_reset_email.delay')  
    def test_send_mail_is_called_on_save(self, mock_send_email):
        """
        Проверяет, что при вызове save() отправляется email через Celery-задачу.
        """
        form = CustomPasswordResetForm(data={'email': 'user@example.com'})
        self.assertTrue(form.is_valid())

        request = self.factory.get(reverse('password_reset')) 
        form.save(request=request, from_email='noreply@example.com')

        self.assertTrue(mock_send_email.called)
        call_args = mock_send_email.call_args[0]
        current_site = get_current_site(request)
        self.assertIn(f'Сброс пароля на {current_site}', call_args[0])  # тема письма
        self.assertIn('http://', call_args[1])  # тело письма
        self.assertEqual(call_args[2], 'noreply@example.com')
        self.assertEqual(call_args[3], ['user@example.com'])

    @patch('accounts.forms.send_password_reset_email.delay')
    def test_save_with_domain_override(self, mock_send_task):
        """
        Проверяет, что при передаче domain_override в тело письма подставляется указанный домен.
        """
        form = CustomPasswordResetForm(data={'email': 'user@example.com'})
        self.assertTrue(form.is_valid())
        form.save(domain_override='example.org', from_email='noreply@example.com')
        self.assertTrue(mock_send_task.called)
        body = mock_send_task.call_args[0][1]
        self.assertIn('example.org', body)