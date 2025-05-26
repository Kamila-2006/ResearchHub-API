from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core import mail
from django.core.cache import cache
from .models import CustomUser


class UserAuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.verify_email_url = reverse('verify-email')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('logout')
        self.password_reset_url = reverse('password-reset')
        self.password_reset_confirm_url = reverse('password-reset-confirm')

        self.user_data = {
            "email": "testuser@example.com",
            "password": "StrongPassw0rd!",
            "password_confirm": "StrongPassw0rd!",
            "first_name": "Test",
            "last_name": "User",
            "institution": "Test Institution",
            "department": "Testing",
            "position": "researcher",
            "orcid_id": "0000-0000-0000-0000"
        }

    def test_user_registration_sends_email_and_caches_data(self):
        """
        Test that user registration sends an email and stores token & user data in cache.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Verification email sent", response.data['detail'])

        # Email yuborilganligini tekshiramiz
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body

        # Emaildagi tokenni olish
        import re
        match = re.search(r'([\w-]{36})', email_body)  # UUID token expected
        token = match.group(1) if match else None

        self.assertIsNotNone(token)

        # Token va email cacheda saqlanganligini tekshirish
        cached_email = cache.get(token)
        self.assertEqual(cached_email, self.user_data["email"])

    def test_email_verification_creates_user(self):
        """
        Test that email verification with a valid token creates a new user.
        """
        token = "test-token"
        email = self.user_data['email']
        user_data = self.user_data.copy()
        user_data.pop('password_confirm')

        cache.set(token, email, timeout=3600)
        cache.set(email, (token, user_data), timeout=3600)

        response = self.client.post(self.verify_email_url, {"token": token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], email)

        # User yaratilganmi tekshiramiz
        user = CustomUser.objects.filter(email=email).first()
        self.assertIsNotNone(user)

    def test_password_reset_request_and_confirm(self):
        """
        Test password reset request and confirmation flow.
        """
        user = CustomUser.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            is_verified=True
        )

        # Reset request
        response = self.client.post(self.password_reset_url, {"email": user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        # Tokenni emaildan olish
        email_body = mail.outbox[0].body
        import re
        match = re.search(r'([\w-]{36})', email_body)
        token = match.group(1) if match else None
        self.assertIsNotNone(token)

        # Reset confirm
        new_password = "NewStrongPass1!"
        response = self.client.post(self.password_reset_confirm_url, {
            "token": token,
            "password": new_password,
            "password_confirm": new_password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parol o‘zgartirilganligini tekshiramiz
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))

    def test_login_logout_flow(self):
        """
        Test JWT login and logout flow.
        """
        user = CustomUser.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            is_verified=True
        )

        # Login
        response = self.client.post(self.login_url, {
            "email": user.email,
            "password": self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data.get('access')
        refresh = response.data.get('refresh')
        self.assertIsNotNone(access)
        self.assertIsNotNone(refresh)

        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.post(self.logout_url, {"refresh": refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_follow_and_unfollow(self):
        """
        Test following and unfollowing another user.
        """
        user1 = CustomUser.objects.create_user(email="user1@example.com", password="pass12345", is_verified=True)
        user2 = CustomUser.objects.create_user(email="user2@example.com", password="pass12345", is_verified=True)

        self.client.force_authenticate(user=user1)

        # Follow
        follow_url = reverse('profile-follow', args=[user2.id])
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(user2.profile, user1.profile.following.all())

        # Unfollow
        unfollow_url = reverse('profile-unfollow', args=[user2.id])
        response = self.client.post(unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(user2.profile, user1.profile.following.all())
