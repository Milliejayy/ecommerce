from django.contrib.auth.backends import ModelBackend
from .models import User

class Auth(ModelBackend):
    def authenticate(self, request,**kwargs):
        user_id = None 

        if kwargs.get("email"):
            user_id = kwargs.get("email")

        if kwargs.get("username"):
            user_id = kwargs.get("username")

        

