from django.contrib import admin
from masterdata.models import Department, Division,RoleStatusMapping
# Register your models here.


admin.site.register(Department)
admin.site.register(Division)
admin.site.register(RoleStatusMapping)