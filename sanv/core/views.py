from django.template import Context, loader
from django.views.generic import TemplateView
from .forms.user import UserRegistrationForm
from django.shortcuts import render, redirect, reverse
from .models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms.auth import *
from .forms.password import *
from django.contrib.auth import login as auth_login, logout as auth_logout

from .backends import authenticate

# Create your views here.


def index(request):
    return render(request, 'core/home.html')


def login(request):
    # User has already logged in
    if request.user.is_authenticated:
        return redirect(reverse('core:home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect(reverse('core:home'))
            else:  # user is not existed or password is incorrect or user is not active
                render(request, 'core/auth/login.html', {'form': form})
        else:
            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'core/auth/login.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    auth_logout(request)
    return redirect(reverse('core:login'))


class UserRegistrationView(TemplateView):
    template_name = 'core/auth/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            # user.assign_default_group()
            user.send_activation_email()
            return redirect(reverse('core:register_success'))
        else:
            return render(request, self.template_name, {'form': form})


def register_success(request):
    return render(request, 'core/auth/register_success.html')


class AccountActivationView(TemplateView):
    template_name = 'core/mail/activate_account.html'

    def get(self, request, token):
        try:
            user = User.objects.get(activation_token=token)
            user.activate()
            return render(request, 'core/auth/activate_account_success.html')
        except User.DoesNotExist:
            return render(request, 'core/auth/activate_account_fail.html')


class PasswordResetView(TemplateView):
    template_name = 'core/auth/password_reset.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            user.send_password_reset_email()
            return render(request, 'core/auth/password_reset_notice.html')

        return render(request, self.template_name, {'form': form})


class NewPasswordView(TemplateView):
    template_name = 'core/auth/new_password.html'

    def get(self, request, token):
        try:
            user = User.objects.get(password_reset_token=token)
            form = NewPasswordForm()
            return render(request, self.template_name, {'form': form})
        except User.DoesNotExist:
            return render(request, 'core/auth/password_reset_nonexist.html')

    def post(self, request, token):
        form = NewPasswordForm(request.POST)

        if form.is_valid():
            user = User.objects.get(password_reset_token=token)
            password = form.cleaned_data.get('password')
            user.reset_password(password)
            return render(request, 'core/auth/password_reset_success.html')

        return render(request, self.template_name, {'form': form})
