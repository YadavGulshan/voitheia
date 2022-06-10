from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from MyUserModel import CustomUserManager
from MyUserModel import UserManager

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(_("email_address"), unique=True, max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def is__str__(self):
        return self.email

    class UserManager(BaseUserManager):
        def create_user(self, email, password=None):
            """
            Creates and saves a User with the given email and password.
            """
            if not email:
                raise ValueError("Users must have an email address")

            user = self.model(
                email=self.normalize_email(email),
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# hook in the New Manager to our Model
class User(AbstractBaseUser):  # from step 2
    ...
    objects = UserManager()
