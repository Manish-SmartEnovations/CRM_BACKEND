from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



# Create your models here.
# class SiteConfig(singletonModel):
#     company_name = models.CharField(
#         default="Your company name", max_length=225)
#     company_email = models.EmailField(default="your-email@example.com")
    
class UserManager(BaseUserManager):
    """Custom auth model"""
    
    def create_user(self, name, email, role=None, password=None):
        
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            role=role
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, name, email, password):
        user = self.create_user(
            name=name,
            email=email,
            password=password
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """Custom User for additional field"""
    
    
    name = models.CharField(max_length=100)
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    
    designation = models.CharField(
        ("Designation"), max_length=50, blank=False, null=True)
    
    
    # employee_image = models.ImageField(
        # upload_to=User_directory_path, blank=True, null=True)
    
    #choice for role
    CEO = 1
    MANAGER = 2
    BDE = 3
    
    ROLE_CHOICES = (
        (CEO, 'CEO'),
        (MANAGER, 'Manager'),
        (BDE, 'BDE')
    )
    
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)
    
    @property
    def is_ceo(self):
        return self.role == self.CEO
    
    @property
    def is_manager(self):
        return self.role == self.MANAGER
    
    @property
    def is_bde(self):
        return self.role == self.BDE
    
    manager = models.ForeignKey('User', default=None, null=True, blank=True,
                             limit_choices_to={'role':MANAGER},
                             on_delete=models.SET_DEFAULT)
    
    department = models.CharField(
        ("Department"), max_length=50, blank=False, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin