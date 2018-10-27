from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    用于验证查询的类中的用户是否为当前用户
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            user = obj.user
        except AttributeError:
            try:
                user = obj.operator
            except AttributeError:
                try:
                    user = obj.author
                except:
                    user = obj.critics
        return user == request.user