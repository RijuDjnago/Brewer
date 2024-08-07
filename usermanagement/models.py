from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

# Create your models here.

class Permission(models.Model):
    """Database model for permission"""
    name = models.CharField(max_length=255, help_text='e.g. user_management')
    display = models.CharField(max_length=255, help_text='e.g. User Management')


class Role(models.Model):
    """Database model for role"""
    role = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.role}'


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")
       
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.username = self.generate_username(first_name)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, password=None):
        user = self.create_user(first_name, last_name, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        if user.is_staff is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if user.is_superuser is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.') 
        user.save(using=self._db)
        return user

    def generate_username(self, first_name):
        username = f"{first_name.lower()}{random.randint(1000, 9999)}"
        while User.objects.filter(username=username).exists():
            username = f"{first_name.lower()}{random.randint(1000, 9999)}"
        return username

  
class User(AbstractBaseUser, PermissionsMixin):
    """Database model for Custom User"""
    first_name = models.CharField(max_length=30, help_text="First name")
    last_name = models.CharField(max_length=30, help_text="Last name")
    phone_number = models.CharField(max_length=15, unique=True, help_text="Phone Number")
    country_code = models.CharField(max_length=5, null=True, blank=True, help_text="Country code")
    username = models.CharField(max_length=50, unique=True, help_text="Username")
    role = models.ManyToManyField(Role, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} - {self.phone_number}'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    
    def get_role_perm(self):
        "returns the custom permissions asssigned to the role"
        role_perm = []
        for role in self.role.all():
            for permission in role.permissions.values_list('display'):
                role_perm.append(permission[0])
                #print(role_perm)
        return role_perm

    def get_role(self):
        user_roles_object = self.role.all()
        role_list = [role_data.role for role_data in user_roles_object]

        return role_list
    

User = get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def generate_otp(self):
        OTP.objects.filter(user=self.user, is_active=True).update(is_active=False)
        
        # Generate a new OTP
        self.otp = f"{random.randint(100000, 999999)}"
        self.is_active = True
        self.created_at = timezone.now()  # Update the created_at time
        self.save()
        return self.otp

    def is_valid(self):
        print(timezone.now(), self.created_at)
        return (timezone.now() - self.created_at).seconds < 3000


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

AGE_GROUP = (
    ('INF', 'Infants (0-2 years)'),
    ('TOD', 'Toddlers (2-4 years)'),
    ('CHI', 'Children (5-12 years)'),
    ('TEEN', 'Teenagers (13-19 years)'),
    ('YAD', 'Young Adults (20-35 years)'),
    ('MAD', 'Middle-Aged Adults (36-55 years)'),
    ('SEN', 'Seniors (56-75 years)'),
    ('ELD', 'Elderly (76+ years)'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    age = models.CharField(max_length=5, choices=AGE_GROUP, default='YAD')

    def __str__(self):
        return f'{self.user.username} | {self.age} | {self.gender}'
    
