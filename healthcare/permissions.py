from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.created_by == request.user


class IsPatientOwner(permissions.BasePermission):
    """
    Custom permission to only allow patient creators to access their patients.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the creator of the patient
        return obj.created_by == request.user


class IsDoctorOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for doctors - allow read access to all, write access to creators only.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the doctor record
        return obj.created_by == request.user
