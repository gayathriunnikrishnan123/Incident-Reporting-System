from django.db import models

# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name




class IncidentStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.name


class IncidentSeverity(models.Model):
    level = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=1)  
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.level
