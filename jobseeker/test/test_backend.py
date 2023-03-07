from django.test import TestCase
from ..backend import CustomBackend
from django.test import Client
from ..models import Users

class UsersManagerTestCase(TestCase):


    def test_authenticate_for_invalid_credentials(self):
        client = Client()
        # username with password does not exist on the database
        result = client.login(username="username",password="password")
        assert result == False

    def test_authenticate_for_valid_credentials(self):
        client = Client()
        Users.objects.create(
            username="username",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )
        result = client.login(username="username",password="password")
        assert result == True

    def test_get_user(self):
        custom_backend = CustomBackend()
        created_user = Users.objects.create(
            username="username",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )
        fetched_user = custom_backend.get_user(created_user.pk)
        assert created_user == fetched_user