from django.template import Context, loader
from django.views.generic import TemplateView
from .forms.user import UserRegistrationForm, UserProfileForm
from django.shortcuts import render, redirect, reverse
from .models import User, UserProfile
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


class UserProfileView(TemplateView):
    template_name = 'core/profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('core:login'))
        if request.user.profile is None:
            form = UserProfileForm()
        else:
            form = UserProfileForm(initial={'job': request.user.profile.job, 'company': request.user.profile.company,
                                            'job_position': request.user.profile.job_position,
                                            'dob': request.user.profile.dob,
                                            'tel': request.user.profile.tel,
                                            'unv_sweden': request.user.profile.unv_sweden,
                                            'major_sweden': request.user.profile.major_sweden})
        return render(request, self.template_name,
                      {'form': form, 'full_name': request.user.get_full_name(), 'email': request.user.email})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('core:login'))
        if request.user.profile is None:
            form = UserProfileForm(data=request.POST or None)
        else:
            form = UserProfileForm(initial={'job': request.user.profile.job, 'company': request.user.profile.company,
                                            'job_position': request.user.profile.job_position,
                                            'dob': request.user.profile.dob,
                                            'tel': request.user.profile.tel,
                                            'unv_sweden': request.user.profile.unv_sweden,
                                            'major_sweden': request.user.profile.major_sweden},
                                   data=request.POST or None)

        print(form.errors)

        if form.is_valid():
            if request.user.profile is None:
                up = UserProfile.objects.create(
                    job=form.cleaned_data['job'],
                    company=form.cleaned_data['company'],
                    job_position=form.cleaned_data['job_position'],
                    dob=form.cleaned_data['dob'],
                    tel=form.cleaned_data['tel'],
                    unv_sweden=form.cleaned_data['unv_sweden'],
                    major_sweden=form.cleaned_data['major_sweden']
                )
                User.objects.filter(id=request.user.id).update(profile=up)
            else:
                UserProfile.objects.filter(id=request.user.profile.id).update(
                    job=form.cleaned_data['job'],
                    company=form.cleaned_data['company'],
                    job_position=form.cleaned_data['job_position'],
                    dob=form.cleaned_data['dob'],
                    tel=form.cleaned_data['tel'],
                    unv_sweden=form.cleaned_data['unv_sweden'],
                    major_sweden=form.cleaned_data['major_sweden']
                )

            return redirect(reverse('core:profile_success'))
        else:
            return render(request, self.template_name,
                          {'form': form, 'full_name': request.user.get_full_name(), 'email': request.user.email})


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


def profile_update_success(request):
    return render(request, 'core/auth/register_success.html')


class AccountActivationView(TemplateView):
    template_name = 'core/mail/activate_account.html'

    def get(self, request, token):
        try:
            user = User.objects.get(request=token)
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
            user = User.objects.get(request=email)
            user.send_password_reset_email()
            return render(request, 'core/auth/password_reset_notice.html')

        return render(request, self.template_name, {'form': form})


class NewPasswordView(TemplateView):
    template_name = 'core/auth/new_password.html'

    def get(self, request, token):
        try:
            user = User.objects.get(request=token)
            form = NewPasswordForm()
            return render(request, self.template_name, {'form': form})
        except User.DoesNotExist:
            return render(request, 'core/auth/password_reset_nonexist.html')

    def post(self, request, token):
        form = NewPasswordForm(request.POST)

        if form.is_valid():
            user = User.objects.get(request=token)
            password = form.cleaned_data.get('password')
            user.reset_password(password)
            return render(request, 'core/auth/password_reset_success.html')

        return render(request, self.template_name, {'form': form})
