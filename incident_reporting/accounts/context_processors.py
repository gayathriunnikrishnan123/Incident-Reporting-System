# accounts/context_processors.py
from .utils import user_is_admin, user_is_reviewer, user_is_responder

def user_roles(request):
    if request.user.is_authenticated:
        return {
            'is_admin': user_is_admin(request.user),
            'is_reviewer': user_is_reviewer(request.user),
            'is_responder': user_is_responder(request.user),
        }
    return {}