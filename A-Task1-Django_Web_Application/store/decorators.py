from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_admin_user:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("store:product_list")
        return view_func(request, *args, **kwargs)
    return wrapper
