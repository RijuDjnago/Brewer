from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='sign-up'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
]