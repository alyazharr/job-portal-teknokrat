from django.test import TestCase
from ..managers import UsersManager
from ..models import Users

class UsersManagerTestCase(TestCase):


    def test_create_user(self):
        manager = UsersManager()
        manager.model = Users
        created_user = manager.create_user(
            "mock password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        assert created_user.npm == 1
        assert created_user.prodi_id == 1
        assert created_user.role_id == 1
        # ensure that the password is hashed
        assert created_user.password != "mock password"

    def test_create_superuser(self):
        manager = UsersManager()
        manager.model = Users
        created_user = manager.create_superuser("password mock",npm=1,prodi_id=1)
        assert created_user.npm == 1
        assert created_user.prodi_id == 1
        # Test to indicate that a user is an admin
        assert created_user.role_id == 4
        # ensure that the password is hashed
        assert created_user.password != "password mock"