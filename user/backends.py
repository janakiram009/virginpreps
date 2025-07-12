from django.contrib.auth.backends import BaseBackend
from .models import User

class PhoneOTPBackend(BaseBackend):
    def authenticate(self, request, phone=None, otp=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        if user.verify_otp(otp):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None