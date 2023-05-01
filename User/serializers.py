from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator, MinLengthValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]{4,10}$', message='Username should be alphanumeric and 4 to 10 characters long')]
    )
    password = serializers.CharField(
        validators=[MinLengthValidator(6), RegexValidator(regex='^(?=.*[A-Z]).{6,12}$', message='Password should be 6 to 12 characters long and contain at least one uppercase letter')]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


