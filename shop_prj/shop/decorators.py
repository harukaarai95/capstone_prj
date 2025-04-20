from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in.")
            if request.user.role not in allowed_roles:
                raise PermissionDenied("You do not have permission.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator