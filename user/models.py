from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from oscar.apps.customer.abstract_models import AbstractUser as OscarAbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import secrets

OTP_EXPIRY_SECONDS = getattr(settings, 'OTP_EXPIRY_SECONDS', 300)  # 5 minutes

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Users must have a phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(OscarAbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = PhoneNumberField(unique=True, verbose_name=_('Phone number'))
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='referrals', verbose_name=_('Referred by')
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    
    objects = UserManager()

    def __str__(self):
        return str(self.phone)
    


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def credit(self, amount):
        self.balance += amount
        self.save()
        # Create transaction record here

    def __str__(self):
        return f"{self.user.phone}'s Wallet"
# Signals to create wallet automatically


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=100)




from oscar.apps.customer.models import * 
