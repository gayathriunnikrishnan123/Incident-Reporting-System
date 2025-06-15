# accounts/utils.py
from accounts.models import Role, DepartmentProfile

def user_is_admin(user):
    return user.is_superuser or DepartmentProfile.objects.filter(
        user=user, 
        role__name__in=['Admin', 'Administrator']
    ).exists()

def user_is_reviewer(user):
    return DepartmentProfile.objects.filter(
        user=user, 
        role__name__in=['Reviewer', 'Supervisor']
    ).exists()

def user_is_responder(user):
    return DepartmentProfile.objects.filter(
        user=user, 
        role__name__in=['Responder', 'First Responder']
    ).exists()

def user_is_registered(user):
    return not (user_is_admin(user) or user_is_reviewer(user) or user_is_responder(user))