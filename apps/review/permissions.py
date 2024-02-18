from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):
    """
    Проверяет, является ли текущий пользователь автором объекта.
    """
    message = 'Вы не являетесь автором этого объекта.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user
