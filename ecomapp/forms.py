from django import forms
from . models import User

class UserForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField()
    first_name = forms.CharField()
    username = forms.CharField()

    last_name = forms.CharField()
    password = forms.CharField()

