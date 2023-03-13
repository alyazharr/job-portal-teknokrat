from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomBackend(BaseBackend):
    def authenticate(self,request, **kwargs):
        user_model = get_user_model()
        """
        Authenticate user from request argument based on
        username and password, return user if it is valid
        """
        username = password = None

        if request != None:
            body = dict(map(lambda x : x.split("="),request.body.decode("utf-8").split("&")))
            username = body['username']
            password = body['password']
        
        username = username or kwargs.pop("username")
        password = password or kwargs.pop("password")

        try:
            user = user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            user_model().set_password(password)
        else:
            if user.check_password(password) :
                return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            user = user_model._default_manager.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        return user