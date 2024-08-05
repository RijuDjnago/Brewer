from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP
from .helpers import send_sms

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']

class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        otp = OTP.objects.create(user=user)
        otp_code = otp.generate_otp()
        print(user.phone_number)
        send_sms(user.phone_number, f"Your OTP code is {otp_code}")
        return user
