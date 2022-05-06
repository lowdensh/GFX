from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **kwargs):
        """
        Create a custom user with the specified details.
        """
        if email is None:
            raise ValidationError(_('Email must not be blank.'))
        if first_name is None:
            raise ValidationError(_('First Name must not be blank.'))
        if last_name is None:
            raise ValidationError(_('Last Name must not be blank.'))
        if password is None:
            raise ValidationError(_('Password must not be blank.'))

        email = self.normalize_email(email)
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        """
        Create a custom superuser (elevated privileges) with the specified details.
        """
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is False:
            raise ValidationError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is False:
            raise ValidationError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, first_name, last_name, password, **kwargs)
        