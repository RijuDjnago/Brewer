from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *

User = get_user_model()

# Create your views here.
class MenuList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'status':'', 'data':[], 'message':None}
        try:
            user_id = request.GET.get('user_id')
            check_user = User.objects.filter(id=user_id)
            if check_user:
                queryset = MenuItem.objects.all()
                serializer = MenuItemSerializer(queryset, many=True)
                data['status'] = status.HTTP_200_OK
                data['message'] = f'Menu list fetched successfully.'
                data['data'] = serializer.data
            else:
                data['status'] = status.HTTP_200_OK
                data['message'] = f'User not found.'
                data['data'] = []
        except Exception as e:
            data['status'] = status.HTTP_200_OK
            data['message'] = f'{str(e)}'
            data['data'] = [] 
        return Response(data)

