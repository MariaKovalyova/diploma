from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

USER_MODEL = get_user_model()  # get User model


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Проверка пароля на совпадение"""
        password: str = attrs.get('password')
        password_repeat: str = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.messages})

        if password != password_repeat:
            raise serializers.ValidationError("Password don't match")

        return attrs

    def create(self, validated_data):
        password: str = validated_data.get('password')
        hashed_password: str = make_password(password)
        validated_data['password'] = hashed_password
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор авторизации"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор информации о пользователе"""
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Проверка на верность ввода старого пароля"""
        user = self.instance
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': 'incorrect password'})

        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise serializers.ValidationError({'new_password': e.messages})

        return attrs

    def update(self, instance, validated_data):
        """Обновление пароля"""
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
