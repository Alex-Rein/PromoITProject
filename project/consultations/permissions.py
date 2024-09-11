from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions, BasePermission


class CustomModelPermission(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# class CustomObjectPermission(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }


# class IsCustomer(BasePermission):
#
#     def has_permission(self, request, view):
#         if 'auth.is_customer' in request.user.get_all_permissions():
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if 'auth.is_customer' in request.user.get_all_permissions():
#             return True
#         return False


# class IsUserGroupPermission(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.groups.filter(name='User'))

