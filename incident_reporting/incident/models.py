from django.db import models
from django.contrib.auth.models import User
# from masterdata.models import Category, Status, Priority, Department, Division

# class IncidentReport(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
#     division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
#     status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, default=1)  # assuming '1' = New
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     location = models.CharField(max_length=255, null=True, blank=True)
#     user_token = models.CharField(max_length=100, unique=True)
#     is_verified = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_deleted = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

