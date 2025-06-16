from django.db import models
from django.contrib.auth.models import (
    User,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from masterdata.models import Department, Division
from accounts.managers import MyCustomUserManager
from django.db.models import Q, UniqueConstraint

# Create your models here.


class CustomUserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(unique=True, max_length=15, null=True, blank=True)
    default_division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )
    default_department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Allows login to admin panel
    is_admin = models.BooleanField(default=False)  # Custom field for our understanding

    is_deleted = models.BooleanField(default=False) # as per meeting 

    objects = MyCustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    class Meta:
        db_table = "CustomUserProfile"

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    level = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Role_Group"

    def __str__(self):
        return self.name


class DepartmentProfile(models.Model):
    user = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE)
    division = models.ForeignKey(
        Division, on_delete=models.PROTECT, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, null=True, blank=True
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "role"],
                condition=Q(division__isnull=True, department__isnull=True),
                name="user already exist with same role and null division, department",
            ),
            UniqueConstraint(
                fields=["user", "division", "role"],
                condition=Q(department__isnull=True),
                name="Unique User-division-role",
            ),
            UniqueConstraint(
                fields=["user", "department", "role"],
                condition=Q(division__isnull=True),
                name="Unique User-department-role",
            ),
            UniqueConstraint(
                fields=["user", "division", "department", "role"],
                name="Already exist",
            ),
        ]
        db_table = "Department_Profile"


class AuditLog(models.Model):
    user_email = models.EmailField(null=True, blank=True)
    function_name = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Audit_Log"
        ordering = ["-timestamp"]
