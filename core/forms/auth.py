from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..models import User
from ..backends import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        help_text='envelope',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'pt-input pt-fill pt-large',
            'placeholder': 'Email',
            'dir': 'auto',
            'type': 'email'
        })
    )
    password = forms.CharField(
        label='Mật khẩu',
        help_text='lock',
        required=True,     
        widget=forms.PasswordInput(attrs={
            'class': 'pt-input pt-fill pt-large',
            'placeholder': 'Mật khẩu',
            'dir': 'auto'
        }),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            msg = 'Email chưa kích  hoạt hoặc email / mật khẩu không đúng'
            self.add_error(None, msg)
        
        return cleaned_data
