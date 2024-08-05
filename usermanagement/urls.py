from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='sign-up'),
]