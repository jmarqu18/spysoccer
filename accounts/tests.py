from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@10code.es", password="leperinho"
        )
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@10code.es")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="test_super", email="test_super@10code.es", password="leperinho"
        )
        self.assertEqual(user.username, "test_super")
        self.assertEqual(user.email, "test_super@10code.es")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
