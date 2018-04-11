from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..models import User
from ..backends import authenticate


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        help_text='envelope',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'pt-input pt-large',
            'placeholder': 'Email',
            'dir': 'auto',
            'type': 'email'
        })
    )

    first_name = forms.CharField(
        label='Họ',
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'pt-input pt-large',
            'placeholder': 'Họ',
            'dir': 'auto',
            'type': 'name'
        })
    )

    last_name = forms.CharField(
        label='Tên',
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'pt-input pt-large',
            'placeholder': 'Tên',
            'dir': 'auto',
            'type': 'name'
        })
    )

    password = forms.CharField(
        label='Mật khẩu',
        help_text='lock',
        required=True,     
        widget=forms.PasswordInput(attrs={
            'class': 'pt-input pt-large',
            'placeholder': 'Mật khẩu',
            'dir': 'auto'
        }),
    )
    password_confirmation = forms.CharField(
        label='Xác nhận mật khẩu',
        help_text='lock',
        required=True,       
        widget=forms.PasswordInput(attrs={
            'class': 'pt-input pt-large',
            'placeholder': 'Xác nhận mật khẩu',
            'dir': 'auto'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        msg = None

        if self._is_email_empty(email):
            msg = "Email không được để trống"
        elif self._is_existed_email(email):
            msg = "Tài khoản với email này đã tồn tại"
        
        if msg is not None:
            self.add_error('email', msg)
            raise ValidationError(msg)
        
        return email
    
    def _is_email_empty(self, email):
        return email is None

    
    def _is_existed_email(self, email):
        """Check if a user with this email is already existed"""
        user = User.objects.filter(email=email).first()
        return user is not None

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()

        # Validate password
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                msg = "Mật khẩu và xác nhận không khớp nhau"
                self.add_error('password_confirmation', msg)
                self.add_error('password', msg)
        
        return cleaned_data

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('password', 'email', 'first_name', 'last_name')