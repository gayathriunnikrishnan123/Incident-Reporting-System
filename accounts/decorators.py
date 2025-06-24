from accounts.models import AuditLog
from django.shortcuts import redirect
from accounts.models import DepartmentProfile
from django.http import HttpResponseForbidden

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



def role_level_required(min_level):
    def decorator(func):
        def dec_wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.is_superuser:
                request.session['role_name'] = 'Admin'
                request.session['role_level'] = 1 
                return func(request, *args, **kwargs)

            if 'role_level' not in request.session:
                highest_dp = (DepartmentProfile.objects.filter(user=request.user,is_active=True,is_deleted=False,role__is_deleted=False).order_by('role__level').first())
                if highest_dp:
                    request.session['role_level'] = highest_dp.role.level
                    request.session['role_name'] = highest_dp.role.name
                else:
                    return HttpResponseForbidden("Not Authorised user")
            if request.session['role_level'] <= min_level:
                response=func(request,*args, **kwargs)
                return response
            return HttpResponseForbidden("Not Authorised user")
        return dec_wrapper
    return decorator
