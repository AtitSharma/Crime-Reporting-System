from django.db import models


from django.contrib.auth.models import BaseUserManager,AbstractUser

# from report.models import PoliceStation






class GenderChoices(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"





class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class CustomUserModel(BaseUserManager):

    '''
        CREATING CUSTOM USER
    '''

    def create_user(self,email,password=None,**extra_fields):
        '''
            Create Normal Users
        '''
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        '''
            Create Super User
        '''
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True ")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        '''
            Super must have all properties of normal user
        '''
        return self.create_user(email,password,**extra_fields)
    

class User(AbstractUser):
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    username = None
    REQUIRED_FIELDS=[]
    objects=CustomUserModel()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,choices=GenderChoices.choices)
    date_of_birth = models.DateField(blank=True,null=True)
    profile_picture = models.ImageField("user",blank=True,null=True)
    about = models.CharField(max_length=255,blank=True,null=True)
    police_station = models.ForeignKey("report.PoliceStation",on_delete=models.SET_NULL,related_name="police_user",blank=True,null=True)
    
    class Meta:
        verbose_name='User'
        verbose_name_plural="Users"


    @property
    def get_full_name(self):
        return self.first_name + self.middle_name + self.last_name if self.middle_name  else self.first_name + self.last_name

    def __str__(self):
        return self.email