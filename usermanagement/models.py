from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser
import datetime
class CustomUser(AbstractUser):
    otp = models.CharField(max_length=4,blank=True,null=True)
    is_user = models.BooleanField(default=False)
    def __str__(self):
        if self.username:
            return self.username
        elif self.email:
            return self.email
        else:
            return f"User {self.id}"

class Otp(models.Model):
    mobile_number = models.CharField(max_length=12)
    otp = models.CharField(max_length=4 )
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return str(self.otp)

class UserDetail(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    username = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=30,unique=True)
    
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.user.username)
    class Meta:
        permissions = (
                        ("view_all_users", "Can view all users"),
                        ("edit_all_users", "Can edit all users"),
                        ("delete_all_users", "Can delete all users"),
                        
                      )
    