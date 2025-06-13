from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from masterdata.models import Department, Division
from accounts.managers import MyCustomUserManager

# Create your models here.


class CustomUserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname=models.CharField(max_length=100)
    phone=models.CharField(unique=True,max_length=15)
    default_department=models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    default_division=models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)



    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Allows login to admin panel
    is_admin = models.BooleanField(default=False)  # Custom field for our understanding

    objects=MyCustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    class Meta:
        db_table='CustomUserProfile'

    def __str__(self):
        return self.email



class Role(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True)


    class Meta:
        db_table='Role_Group'






class DepartmentProfile(models.Model):
    user = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'department', 'role')
        db_table='Department_Profile'

