from django.contrib import admin
from accounts.models import CustomUserProfile, DepartmentProfile, Role
# Register your models here.


admin.site.register(CustomUserProfile)
admin.site.register(DepartmentProfile)
admin.site.register(Role)

