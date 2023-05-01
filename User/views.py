from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from User.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        if username=="" and email=="":
            return Response({'message': 'username and password are empty.'}, status=status.HTTP_401_UNAUTHORIZED)
        if password=="":
            return Response({'message': 'password can not be empty.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        auth_id = username if username else email
        user = authenticate(request, username=auth_id, password=password)
        if user is not None:
            # user = User.objects.filter(username=user).first()
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response(
                {'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                "username":user.username,
                "email":user.email,
                })
        else:
            return Response({'message': 'Invalid username/email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
