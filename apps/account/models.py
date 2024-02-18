from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
from django.contrib.auth.models import PermissionsMixin


# класс UserManager для управления созданием пользователей
class UserManager(BaseUserManager):

    # приватный метод _create для создания и сохранения пользователя
    def _create(self, email, password, **extra_fields):
        # проверяем, что электронная почта не пуста
        if not email:
            raise ValueError(
                'Email field cannot be empty'
            )
        # нормализуем электронную почту
        email = self.normalize_email(email)
        # создаем пользователя с заданными полями и устанавливаем пароль
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # метод create_user для создания обычного пользователя
    def create_user(self, email, password, **extra_fields):
        # устанавливаем значение по умолчанию для is_staff
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    # метод create_superuser для создания суперпользователя
    def create_superuser(self, email, password, **extra_fields):
        # устанавливаем значения по умолчанию для is_staff и is_active
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


# модель пользователя User, наследующая AbstractBaseUser и PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    # поле email используется в качестве primary key
    email = models.EmailField(primary_key=True)
    # поле name для имени пользователя
    name = models.CharField(max_length=20)
    # поле last_name для фамилии пользователя
    last_name = models.CharField(max_length=30, blank=True)
    # поле is_active для активности пользователя (по умолчанию False)
    is_active = models.BooleanField(default=False)
    # поле is_staff для статуса персонала (по умолчанию False)
    is_staff = models.BooleanField(default=False)
    # оле activation_code для кода активации
    activation_code = models.CharField(max_length=20, blank=True)
    # поле is_brand для статуса бренда (по умолчанию False)
    is_brand = models.BooleanField(default=False)
    # поле brand для названия бренда
    brand = models.CharField(max_length=40, blank=True)

    # присваиваем объекту UserManager наш пользовательский менеджер
    objects = UserManager()

    # указываем поле, используемое для входа в систему
    USERNAME_FIELD = 'email'
    # указываем обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = ['name']

    # роверяем, имеет ли пользователь права на доступ к приложениям
    def has_module_perms(self, app_label):
        return self.is_staff

    # проверяем, имеет ли пользователь определенное разрешение
    def has_perm(self, perm, obj=None):
        return self.is_staff

    # метод для генерации кода активации пользователя
    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()

    # строковое представление объекта пользователя
    def __str__(self):
        return self.email
