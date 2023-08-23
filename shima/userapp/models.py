from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user
    def create_superuser(self, email, password,**extra_fields):
        """ Create a new superuser profile """
        user = self.create_user(email, password,**extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class Users(AbstractBaseUser,PermissionsMixin):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    name=models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    aadhar_number = models.BigIntegerField(null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True)
    gender = models.CharField(choices=GENDERS, max_length=30, null=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True)
    age=models.IntegerField(null=True)
    guardian_name = models.CharField(max_length=120,null=True)
    guardian_contact_number = models.BigIntegerField(null=True)
    number = models.BigIntegerField(verbose_name='phone number', null=True)
    married = models.BooleanField(default=False)
    alternate_number = models.BigIntegerField(null=True)
    is_form_filled = models.BooleanField(default=False)
    last_payment = models.DateField(verbose_name='Fees paid', auto_now=False, auto_now_add=False, null=True)
    is_staff=models.BooleanField(default=False)
    address=models.CharField(max_length=350,null=True)
    pincode=models.CharField(max_length=10,null=True)
    post=models.CharField(max_length=100,null=True)

    # Additional fields or methods can be added here

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = [] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class leave_application(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    start=models.DateField(auto_now=False, auto_now_add=False)
    end=models.DateField(auto_now=False, auto_now_add=False)
    reasone=models.CharField( max_length=500)
    is_approved=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
# class NotificationContent(models.Model):
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
# class Notification(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     content = models.ForeignKey(NotificationContent, on_delete=models.CASCADE)
#     is_seen=models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user}: {self.content__message}"

class Attendance(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.date}"