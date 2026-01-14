from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
import datetime

class CustomUserManager(UserManager):
    def create_user(self, phone, password=None, **extra_field):
        user = self.model(
            phone=phone,
            password=password,
            **extra_field
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_field):
        extra_field['is_superuser'] = True
        extra_field['is_staff'] = True
        return self.create_user(phone=phone, password=password, **extra_field)

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    fullname = models.CharField(max_length=56)
    age = models.PositiveIntegerField(default=0)
    gender = models.BooleanField(default=True, choices=[
        (True, '♂️Erkak'),
        (False, '♀️Ayol'),
    ])


    date_joined = models.DateTimeField(auto_now_add=True)

    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['fullname',]
    USERNAME_FIELD = 'phone'

    def get_name(self):
        return self.fullname or self.phone

class Otp(models.Model):
    token = models.CharField(max_length=256, unique=True)
    phone = models.CharField(max_length=15)

    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)

    extra = models.JSONField(default=dict)
    by = models.SmallIntegerField(choices=[
        (1, 'login'),
        (2, 'register'),
    ])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        if self.is_confirmed:
            self.is_expired = True

        return super(Otp, self).save(*args, **kwargs)

    def vaqt_bormi(self):
        now = datetime.datetime.now()
        if (now - self.created).total_seconds() >= 100:
            return False
        return True










