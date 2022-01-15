from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError


class UsernameField(CharField):
    def validate(self, value):
        super().validate(value)
        if value == '123':
            raise ValidationError("No 123, please!!")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AskForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()


class SignupForm(forms.Form):
    login = forms.CharField()
    email = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if super().is_valid():
            if cleaned_data['password'] != cleaned_data['password_repeat']:
                self.add_error('password_repeat', "Passwords aren't equal")
        return cleaned_data