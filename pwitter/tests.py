from django.http import Http404
from django.test import TestCase

from pwitter.forms import ChangeProfilepicForm
from pwitter.models import *
from pwitter.views import *
from django.contrib.auth.models import User
from pwitter.forms import ChangeProfilepicForm


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

    def test_pweet_delete(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        pweet.save()
        pweet.delete()
        self.assertEqual(len(Pweet.objects.filter(body='test123')), 0)

    def test_reply_pweet_create(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        pweet.save()
        reply = PweetReply(user=user, pweet=pweet, reply_body='reply')
        reply.save()
        self.assertEqual(PweetReply.objects.get(reply_body='reply'), reply)

    def test_pweet_delete_deletes_reply(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        pweet.save()
        reply = PweetReply(user=user, pweet=pweet, reply_body='reply')
        reply.save()
        Pweet.objects.get(body='test123').delete()
        self.assertEqual(len(PweetReply.objects.filter(reply_body='reply')), 0)

    def test_like_post(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        pweet.save()
        pweet.likes.add(user)
        self.assertEqual(pweet.likes.count(), 1)

    def test_unlike_post(self):
        user = create_user()
        pweet = Pweet(user=user, body='test123')
        pweet.save()
        pweet.likes.add(user)
        pweet.likes.remove(user)
        self.assertEqual(pweet.likes.count(), 0)


