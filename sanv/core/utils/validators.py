from __future__ import unicode_literals
from django.conf import settings


def is_valid_email_domain(email):
    """Validate if the email is belonged to allowed domains"""
    for domain in settings.ACCEPTED_EMAIL_DOMAINS:
        if email.endswith(domain):
            return True
    return False
