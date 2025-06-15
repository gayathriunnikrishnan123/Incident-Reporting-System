from accounts.models import AuditLog

def audit_trail_decorator(func):
    def audit_trial_wrapper(request,*args, **kwargs):
        response=func(request,*args, **kwargs)
        auditLog=AuditLog()
        auditLog.user_email=request.user.email if request.user.is_authenticated else 'Anonymous User'
        auditLog.function_name=func.__name__
        auditLog.action="Accessed"
        auditLog.path=request.path
        auditLog.message=f"{func.__name__} returned status {response.status_code}"
        auditLog.save()
        return response
    return audit_trial_wrapper


# accounts/decorators.py
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import user_is_admin, user_is_reviewer, user_is_responder

def role_required(role_check_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
                
            if role_check_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator

# Specific role decorators
def admin_required(view_func):
    return role_required(user_is_admin)(view_func)

def reviewer_required(view_func):
    def check_reviewer(user):
        return user_is_admin(user) or user_is_reviewer(user)
    return role_required(check_reviewer)(view_func)

def responder_required(view_func):
    def check_responder(user):
        return user_is_admin(user) or user_is_reviewer(user) or user_is_responder(user)
    return role_required(check_responder)(view_func)

