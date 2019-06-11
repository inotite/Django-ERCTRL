from django.core.exceptions import PermissionDenied


def administration_required(function):

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            raise PermissionDenied
        elif user.is_superuser or user.profile.is_administrator():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def superadmin_required(function):

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            raise PermissionDenied
        elif user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
