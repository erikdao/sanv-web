from django.contrib.auth.hashers import check_password

from .models import User


class EmailAuthenticationBackend(object):
    """
    Authenticate user by email and password
    """

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)

            if not user.is_active:
                return None

            if check_password(password, user.password):
                return user

            return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


def authenticate(email=None, password=None):
    backend = EmailAuthenticationBackend()
    return backend.authenticate(email=email, password=password)
