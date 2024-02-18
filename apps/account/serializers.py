from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail

User = get_user_model()


# Ссриализатор для регистрации пользователей
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Поле для email
    password = serializers.CharField(min_length=8, required=True)  # Поле для пароля
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)  # Подтверждение пароля
    name = serializers.CharField(required=True)  # Имя пользователя
    last_name = serializers.CharField(required=False, write_only=True)  # Фамилия пользователя
    is_active = serializers.BooleanField(read_only=True)  # Флаг активности

    # валидация уникальности email
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exists')
        return email

    # валидация паролей
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    # создание пользователя
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user


# сериализатор для активации пользователя
class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()  # поле для email
    code = serializers.CharField()  # поле для кода активации

    # валидация email и кода активации
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User not found')
        return attrs

    # активация пользователя
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


# сериализатор для аутентификации
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Поле для email
    password = serializers.CharField(required=True)  # Поле для пароля

    # валидация email
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    # валидация email и пароля
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        if email and password:
            user = authenticate(
                request,
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Incorrect email or password')
        attrs['user'] = user
        return attrs


# сериализатор для изменения пароля
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, required=True)  # Старый пароль
    new_password = serializers.CharField(min_length=8, required=True)  # Новый пароль
    new_password_confirm = serializers.CharField(min_length=8, required=True)  # Подтверждение нового пароля

    # валидация старого пароля
    def validate_old_password(self, old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Enter the correct password')
        return old_pass

    # валидация нового пароля
    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        old_pass = attrs.get('old_password')

        if new_pass1 != new_pass2:
            raise serializers.ValidationError('Passwords do not match')

        if old_pass == new_pass1:
            raise serializers.ValidationError('Passwords match')

        return attrs

    # установка нового пароля
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


# сериализатор для восстановления пароля
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Поле для email

    # валидация email
    def validate_email(self, email):
        if not User.objects.filter(email=email):
            raise serializers.ValidationError('User not found')
        return email

    # отправка письма с кодом восстановления
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Password Recovery',
            f'Your recovery code: {user.activation_code}',
            'test@gmail.com',
            [email]
        )


# сериализатор для завершения восстановления пароля
class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Поле для email
    code = serializers.CharField(required=True)  # Поле для кода восстановления
    password = serializers.CharField(required=True, min_length=8)  # Новый пароль
    password_confirm = serializers.CharField(required=True, min_length=8)  # Подтверждение нового пароля

    # валидация email, кода восстановления и паролей
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User not found')
        if p1 != p2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    # установка нового пароля
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()
