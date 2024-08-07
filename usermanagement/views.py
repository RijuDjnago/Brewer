from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import OTP

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "phone_number": user.phone_number,
                "message": "User created, OTP sent",
            }, status=status.HTTP_201_CREATED)

        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():

            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(phone_number=phone_number)
                otp_instance = OTP.objects.get(user=user, otp=otp)
                if otp_instance.is_valid():
                    user.is_verified = True
                    user.save()
                    otp_instance.is_active = False
                    otp_instance.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message':'OTP verfied successfully.',                        
                        'user_id': user.id,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({"message": "Invalid OTP or phone number"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"message": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"message": "User with this phone number does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        otp_instance, created = OTP.objects.get_or_create(user=user)
        otp_code = otp_instance.generate_otp()  # Generate a new OTP
        send_sms(user.phone_number, f"Your OTP code is {otp_code}")

        return Response({"message": "OTP sent", 'phone_number':user.phone_number}, status=status.HTTP_200_OK)
