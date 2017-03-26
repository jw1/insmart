from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginTestSuite(TestCase):

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()

    def test_good_login(self):
        user = authenticate(username="john", password="johnpassword")
        self.assertIsNotNone(user)

    def test_invalid_login(self):
        user = authenticate(username="john", password="boo_i_forgot")
        self.assertIsNone(user)

    def test_good_login_and_logout(self):
        user = authenticate(username="john", password="johnpassword")
        self.assertIsNotNone(user)


