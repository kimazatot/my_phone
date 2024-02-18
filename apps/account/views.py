from rest_framework.views import APIView  # Импорт базового класса для создания API-вью
from rest_framework.response import Response  # Импорт класса для формирования HTTP-ответов
from .serializers import *  # Импорт всех сериализаторов из модуля
from rest_framework.authtoken.views import ObtainAuthToken  # Импорт вида для получения токена аутентификации
from rest_framework.permissions import IsAuthenticated  # Импорт класса для проверки аутентификации пользователей
from rest_framework.authtoken.models import Token  # Импорт модели токена аутентификации
from drf_yasg.utils import swagger_auto_schema  # Импорт декоратора для автоматической генерации документации в Swagger


class RegistrationView(APIView):

    # Декоратор для автоматической генерации документации Swagger для метода POST
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)  # Создание экземпляра сериализатора с данными запроса
        serializer.is_valid(raise_exception=True)  # Проверка валидности данных, при необходимости генерация исключения
        serializer.save()  # Сохранение данных
        return Response('Account has been successfully created',
                        status=201)


class ActivationView(APIView):

    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(
                raise_exception=True):
            serializer.activate()  # Активация пользователя
            return Response('User has been activated',
                            status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer  # Использование сериализатора для аутентификации


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Установка прав доступа: пользователь должен быть аутентифицирован

    # Метод для обработки запросов типа DELETE
    def delete(self, request):
        user = request.user  # Получение текущего пользователя из запроса
        Token.objects.filter(user=user).delete()  # Удаление токена аутентификации пользователя
        return Response(
            'You have successfully logged out')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={
            'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been changed',
                        status=200)


class ForgotPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_verification_email()  # Отправка письма с кодом восстановления пароля
        return Response('Password recovery code has been sent to your email',
                        status=200)


class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been changed',
                        status=200)