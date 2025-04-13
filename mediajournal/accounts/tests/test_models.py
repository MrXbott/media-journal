from django.test import TestCase, override_settings
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import shutil

from accounts.models import User
from articles.models import Article 


TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        Article.objects.create(title='Moderation Article', author=cls.user, status=Article.Status.MODERATION)
        Article.objects.create(title='Published Article', author=cls.user, status=Article.Status.PUBLISHED)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.photo.name, 'default/default_user_photo.jpg')

    def test_unique_email_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(username='anyuser', email=self.user.email, password='password456')

    def test_unique_username_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(username=self.user.username, email='anyemail@example.com', password='password456')

    def test_optional_fields(self):
        optional_designation = 'Engineer'
        optional_bio = 'A short bio.'

        user = User.objects.create(
            username='username',
            email='email@example.com',
            password='pass123',
            designation=optional_designation,
            bio=optional_bio
        )
        self.assertEqual(user.designation, optional_designation)
        self.assertEqual(user.bio, optional_bio)

    def test_str_returns_email(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_save_generates_username(self):
        user = User.objects.create(email='newmail@example.com', password='password123')
        self.assertTrue(user.username.startswith('newmail'), "Username должен начинаться с части email")
        self.assertTrue(user.username[7:].isdigit(), "После 'newmail' должно быть случайное число")

    def test_get_absolute_url(self):
        expected_url = reverse('profile', kwargs={'id': self.user.id})
        self.assertEqual(self.user.get_absolute_url(), expected_url)

    def test_photo_upload(self):
        image_name = 'photo.jpg'
        image = SimpleUploadedFile(image_name, b'\x47\x49\x46\x38\x89\x61', content_type='image/jpeg')
        user = User.objects.create(
            username='user',
            email='email@example.com',
            password='password123',
            photo=image
        )
        self.assertTrue(user.photo.name, image_name)

    def test_following_relationship(self):
        user1 = User.objects.create(username='user1', email='user1@example.com', password='pass123')
        user2 = User.objects.create(username='user2', email='user2@example.com', password='pass456')
        user1.following.add(user2)
        self.assertIn(user2, user1.following.all())
        self.assertIn(user1, user2.followers.all())

    def test_user_published_articles_property(self):
        self.assertEqual(self.user.published_articles.count(), 1)
        expected_queryset = Article.objects.filter(author=self.user, status=Article.Status.PUBLISHED)
        self.assertQuerySetEqual(self.user.published_articles, expected_queryset)




