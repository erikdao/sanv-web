from __future__ import unicode_literals

import logging
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings


def send_mail(
        from_email=None, subject=None,
        to_email=None, content=None):
    """Send email to a specific email address using Sendgrid"""
    import urllib.error

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.error.HTTPError as e:
        logging.error(e)
        return e
    except Exception as e:
        logging.error(e)


def _make_token_link(path, token):
    return "{}/{}/{}/".format(
        settings.CANONICAL_URL,
        path,
        token
    )


def make_account_token_link(token):
    """Create an account activation link from a given token"""
    return _make_token_link('activate_account', token)


def make_password_reset_link(token):
    """Create an account activation link from a given token"""
    return _make_token_link('password_reset', token)


def is_email_exist(email):
    from ..models import User
    try:
        user = User.objects.get(request=email)
        return user is not None
    except User.DoesNotExist:
        return False
