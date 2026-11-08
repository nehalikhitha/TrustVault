from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="TestPass@123"
        )

        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("TestPass@123"))

    def test_user_role_default(self):
        user = User.objects.create_user(
            username="vieweruser",
            password="TestPass@123"
        )

        self.assertIsNotNone(user.role)