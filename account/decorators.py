from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from account.models import Profile


def profile_required(path):
    """
    Decorator to check if request.user has an entry in Profile model.

    Usage:
        @billing_required(path)
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # return HttpResponseForbidden("User not authenticated")
                return view_func(request, *args, **kwargs)
            try:
                if Profile.objects.filter(user=request.user).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect(f"{path}?next={request.get_full_path()}")
            except Exception as e:
                return HttpResponseForbidden(str(e))

        return _wrapped_view

    return decorator
