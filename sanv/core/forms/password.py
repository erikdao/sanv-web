from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..models import User
from ..backends import authenticate


class PasswordResetForm(forms.Form):
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

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()

        email = cleaned_data.get('email')

        try:
            user = User.objects.get(request=email)
        except User.DoesNotExist:
            msg = 'Không tồn tại tài khoản với email này. Xin ' \
                  'vui lòng kiểm tra lại.'
            self.add_error(None, msg)
        finally:
            return cleaned_data


class NewPasswordForm(forms.Form):
    password = forms.CharField(
        label='Mật khẩu mới',
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

    def clean(self):
        cleaned_data = super(NewPasswordForm, self).clean()

        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('password_confirmation')

        if password and confirmation:
            if password != confirmation:
                msg = 'Mật khẩu và xác nhận không trùng khớp'
                self.add_error('password', msg)
                self.add_error('password_confirmation', msg)
        
        return cleaned_data