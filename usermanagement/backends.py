from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import OTP
from django.db.models import Q

User = get_user_model()

class OTPBackend(BaseBackend):
    def authenticate(self, request, username=None, otp=None):
        try:
            user = User.objects.get(Q(username=username) | Q(phone_number=username))
        except User.DoesNotExist:
            return None

        otp_instance = OTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()
        if otp_instance and otp_instance.is_valid():
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
