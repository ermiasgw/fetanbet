from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.password_validation import validate_password
from .utils import sendemailconfirmation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'email', 'groups']

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField() 
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, value):
        if value["password1"] != value["password2"]:
            raise serializers.ValidationError('incorrect password confirmation')
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password1'],
            is_active=False,
            )

        sendemailconfirmation(user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


