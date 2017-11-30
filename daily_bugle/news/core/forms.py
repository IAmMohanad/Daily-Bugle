from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
#from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
#widget=forms.PasswordInput(attrs={'class':'form2'}) not working
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=254, help_text="Required. Please enter a valid email.")
    phone_number = forms.IntegerField(max_length=20)

    USERNAME_FIELD = 'email'

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "phone_number")

    def save(self, **kwargs):
        self.clean()
        return super(SignUpForm, self).save(**kwargs)

    def clean(self):
        #cd = self.cleaned_data
        print("beg")
        cd = super(SignUpForm, self).clean()
        print("khjkhjkh")
        #phoneNumber = cd.get('phone_number')
        #if not phoneNumber.isdigit():
            #pass
        self.add_error('phone_number', "Phone number must be numerical.")
        self.add_error('first_name', "Phone number must be numerical.")
        self.add_error('last_name', "Phone number must be numerical.")
        self.add_error('email', "Phone number must be numerical.")
        return cd

class LogInForm():
    email = forms.EmailField(max_length=254, help_text="Required. Please enter a valid email.")
