from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from .helpers import send_sms
from rest_framework import status

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
        phone_number = validated_data['phone_number']
        
        if User.objects.filter(phone_number=phone_number).exists():
            phone_number = User.objects.get(phone_number=phone_number).phone_number
            raise serializers.ValidationError({"message": "Phone number already exists.", "phone_number":phone_number, "status":status.HTTP_400_BAD_REQUEST})
        role = Role.objects.filter(role='Customer').first()
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        if role:
            user.role.add(role)
        else:
            raise serializers.ValidationError({
                "message": "Customer role does not exist.",
                "status": status.HTTP_400_BAD_REQUEST
            })
        otp = OTP.objects.create(user=user)
        otp_code = otp.generate_otp()
        print(user.phone_number)
        send_sms(user.phone_number, f"Your OTP code is {otp_code}")
        return user

