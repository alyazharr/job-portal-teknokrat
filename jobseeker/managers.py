
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UsersManager(BaseUserManager):
    """
    Custom User Manager to integrate Users model to 
    django authentication system
    """
    def create_user(self, password, **extra_fields):
        """
            creates user as Users instance and saves it on the database.
        """
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault("role_id",4)

        return self.create_user(password,**extra_fields)
    
    def create(self,**kwargs):
        return self.create_user(kwargs.pop("password"),**kwargs)