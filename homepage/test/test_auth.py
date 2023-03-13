from django.test import TestCase, Client
from jobseeker.models import Users
from django.urls import reverse

class AuthenticationTest(TestCase):

    def setUp(self):
        global HOMEPAGE_LOGIN
        HOMEPAGE_LOGIN = "homepage:login"

        global HOMEPAGE_LOGOUT
        HOMEPAGE_LOGOUT = "homepage:logout"

        global HOMEPAGE_HOME
        HOMEPAGE_HOME = "homepage:home"

        self.client = Client()
        self.username = "testuser"
        self.password = "testpass"
        self.user = Users.objects.create(
            username=self.username,
            password=self.password,
            npm=1,
            prodi_id=1,
            role_id=1
        )


    def test_login_view(self):
        # Make sure the login view use the right template and succeed
        response = self.client.get(reverse(HOMEPAGE_LOGIN))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_success_login(self):
        # User success log in
        response = self.client.post(reverse(HOMEPAGE_LOGIN), {'username':self.username, 'password':self.password})
        self.assertRedirects(response, reverse(HOMEPAGE_HOME))

    def test_fail_login(self):
        # User fail log in
        response = self.client.post(reverse(HOMEPAGE_LOGIN), {'username':self.username, 'password':"wrongpass"})
        self.assertRedirects(response, reverse(HOMEPAGE_LOGIN))

    def test_logout_view(self):
        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Log out the user
        response = self.client.get(reverse(HOMEPAGE_LOGOUT))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(HOMEPAGE_LOGIN))