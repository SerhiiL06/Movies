from functools import wraps

from service.exceptions import PermissionDenied


def check_role(allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user.get("role") not in allowed_roles:
                raise PermissionDenied()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
