"""sanv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views
from .views import *

app_name = 'core'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('register/', view=UserRegistrationView.as_view(), name="register"),
    path('register/success/', view=register_success, name="register_success"),
    path('login/', view=login, name="login"),
    path('logout/', view=logout, name="logout"),
    path(
        'password_reset/<slug:token>/',
        view=NewPasswordView.as_view(),
        name="new_password"
    ),
    path('password_reset/', view=PasswordResetView.as_view(), name="password_reset"),
    path(
        'activate_account/<slug:token>/',
        view=AccountActivationView.as_view(),
        name="activate_account"
    ),
]
