from .models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name")
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError(" your passwords not match!")
        return cd["password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        cd = self.cleaned_data
        user.set_password(cd["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you cant changed using <a href=\"../password/ \"> this form </a> ")
    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name","password", "last_login")
        
        
class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length=50)
    password = forms.CharField(label = "password", widget=forms.PasswordInput)


