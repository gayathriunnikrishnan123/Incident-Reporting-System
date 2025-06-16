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