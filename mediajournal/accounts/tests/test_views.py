from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from unittest.mock import patch

from accounts.token import email_verification_token
from accounts.models import User


class AccountsViewsTests(TestCase):
    
    def setUp(self):
        """
        Создаёт тестового пользователя и клиент для отправки запросов.
        """
        self.client = Client()
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        self.user.save()

    def test_registration_view_get(self):        
        """
        Проверяет, что GET-запрос к представлению регистрации возвращает 
        шаблон registration.html и статус 200.
        """
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')


    @patch('accounts.views.send_confirm_email.delay')
    def test_registration_view_post_valid(self, mock_send_email):
        """
        Проверяет успешную регистрацию пользователя: 
        создание объекта User, отправку письма и правильный шаблон.
        """
        data = {
            'email': 'new@example.com',
            'password1': 'pass123!worD',
            'password2': 'pass123!worD'
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='new@example.com').exists())
        self.assertTrue(mock_send_email.called)
        self.assertTemplateUsed(response, 'registration/email_confirmation.html')


    def test_registration_post_invalid(self):
        """
        Проверяет, что при невалидных данных форма возвращается с ошибкой и 
        остаётся на странице регистрации.
        """
        invalid_data = {
            'email': 'new@example.com',
            'password1': 'pass123!worD',
            'password2': 'PPass123!worD'
        }
        response = self.client.post(reverse('registration'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')
        self.assertContains(response, 'При создании аккаунта возникла ошибка')
        

    def test_confirm_email_valid_token(self):
        """
        Проверяет успешную активацию аккаунта при корректном токене и uid.
        """
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        token = email_verification_token.make_token(self.user)
        url = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration_done.html')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    
    def test_confirm_email_invalid_token(self):
        """
        Проверяет отображение страницы ошибки активации при невалидном токене.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = 'invalid-token'
        url = reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTemplateUsed(response, 'registration/activation_error.html')

    
    def test_confirm_email_invalid_uid(self):
        """
        Проверяет обработку ошибки при некорректном uid в ссылке подтверждения.
        """
        wrong_user_id = 999999
        uidb64 = urlsafe_base64_encode(force_bytes(wrong_user_id)) 
        token = email_verification_token.make_token(self.user)
        url = reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTemplateUsed(response, 'registration/activation_error.html')


    @patch('accounts.views.User.objects.get')
    def test_confirm_email_exception(self, mock_get):
        """
        Проверяет поведение при исключении в User.objects.get (например, ValueError).
        """
        mock_get.side_effect = ValueError('bad uid') # эмулируем ошибку при получении пользователя
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = email_verification_token.make_token(self.user)
        url = reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'registration/activation_error.html')


    def test_profile_view(self):
        """
        Проверяет, что профиль доступен по ID пользователя и 
        возвращает нужный шаблон.
        """
        url = reverse('profile', kwargs={'id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')


    def test_edit_profile_view_get(self):
        """
        Проверяет, что GET-запрос к форме редактирования профиля работает 
        для авторизованного пользователя.
        """
        logged_in = self.client.login(username='test@example.com', password='password123')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_edit.html')
        self.assertIn('form', response.context)


    def test_edit_profile_not_authenticated(self):
        """
        Проверяет, что неавторизованный пользователь перенаправляется на страницу логина 
        при попытке редактировать профиль.
        """
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    
    def test_edit_profile_post_valid_data(self):
        """
        Проверяет, что профиль успешно обновляется при валидных данных и 
        происходит редирект на страницу профиля.
        """
        logged_in = self.client.login(username='test@example.com', password='password123')
        self.assertTrue(logged_in)
        new_data = {
            'username': 'new_username',
            'designation': 'new designation',
            'bio': 'new bio'
        }
        response = self.client.post(reverse('edit_profile'), new_data, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.designation, 'new designation')
        self.assertEqual(self.user.bio, 'new bio')
        self.assertRedirects(response, reverse('profile', args=[self.user.id]))

    
    def test_edit_profile_post_invalid_data(self):
        """
        Проверяет, что при невалидных данных форма редактирования возвращается с ошибками.
        """
        logged_in = self.client.login(username='test@example.com', password='password123')
        self.assertTrue(logged_in)
        invalid_data = {
            'username': '',  # username обязателен
        }
        response = self.client.post(reverse('edit_profile'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_edit.html')
        self.assertTrue(response.context['form'].errors)