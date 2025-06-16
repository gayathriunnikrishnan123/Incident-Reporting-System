from django.contrib.auth.models import BaseUserManager



class MyCustomUserManager(BaseUserManager):
    
    def create_user(self,email,password=None,**kwargs):

        if not email:
            raise ValueError("Email should not be empty")
        email=self.normalize_email(email)
        user_instance=self.model(email=email,**kwargs)
        user_instance.set_password(password)
        user_instance.save(using=self._db)
        return user_instance
    
    def create_superuser(self,email,password,**kwargs):
        if not password:
            raise ValueError('Superusers must have a password.')
        
        kwargs.setdefault('is_active',True)
        kwargs.setdefault('is_admin',True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True) 

        if kwargs.get('is_active') is not True:
            raise ValueError("is active must be true for super user")
        if kwargs.get('is_admin') is not True:
            raise ValueError("admin should be true for superuser")
        if kwargs.get('is_staff') is not True:
            raise ValueError("Superuser must be staff.")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("is_superuser must be True for superuser.")
        
        return self.create_user(email,password,**kwargs)