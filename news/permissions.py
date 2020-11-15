from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """permission to edit only the author"""

    def has_object_permission(self, request, view, vacation_obj):
        return request.method in SAFE_METHODS or vacation_obj.author == request.user


class IsMe(BasePermission):
    """permission to edit a user only for the same user"""

    def has_object_permission(self, request, view, vacation_obj):
        print("vacation_obj == request.user")
        print(vacation_obj, "==", request.user)
        print(vacation_obj == request.user)
        return vacation_obj == request.user
