from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class Createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean(self):
        password1=self.cleaned_data['password1']
        if len(password1)<=8:
            raise forms.ValidationError("password should contain atleast 8 char")
        
        if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password1):
            raise forms.ValidationError("Password should contain at least one special character.")

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password should contain at least one numeric character.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Both passwords do not match.")


