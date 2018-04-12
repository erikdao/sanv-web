import uuid
import logging
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save user with given email and password"""
        if not email:
            raise ValueError('The given email must be set!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.activation_token = uuid.uuid4().hex[:32] # Generate activation code
        user.set_password(password)
        user.save(using=self._db)       
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)
