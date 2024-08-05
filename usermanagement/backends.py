from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import OTP
from django.db.models import Q

User = get_user_model()
class OTPBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, otp=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            if otp:
                otp_record = OTP.objects.filter(user=user).latest('created_at')
                if otp_record and otp_record.otp == otp and otp_record.is_valid():
                    return user
            elif password:
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None
        except OTP.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None