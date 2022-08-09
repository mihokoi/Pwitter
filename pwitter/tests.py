from django.test import TestCase
from pwitter.models import *
from django.contrib.auth.models import User


def create_user():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return user


class PweetTestCase(TestCase):
    def test_pweet_create(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        self.assertEqual(pweet.body, "test123")
        self.assertEqual(pweet.user, user)
