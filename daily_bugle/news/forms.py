from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
#from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=254, help_text="Required. Please enter a valid email.")
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number")
