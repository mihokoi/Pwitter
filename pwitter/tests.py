from django.http import Http404
from django.test import TestCase

from pwitter.forms import ChangeProfilepicForm
from pwitter.models import *
from django.contrib.auth.models import User


def create_user():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return user


class PweetTestCase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.kwargs = None

    def test_pweet_create(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        self.assertEqual(pweet.body, "test123")
        self.assertEqual(pweet.user, user)


