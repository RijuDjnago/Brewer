from django.urls import path
from .views import *

urlpatterns = [
    path('menu-list/', MenuList.as_view(), name='menu-list'),
    
]
