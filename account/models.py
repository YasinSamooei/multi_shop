from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
#---------------------------------------------------------------------------------------------------------------
#customize User model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email-adress',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    full_name = models.CharField(verbose_name="fullname", max_length=50,blank = True , null = True)
    username = models.CharField(verbose_name="username", max_length=50,blank = True , null = True)
    is_active = models.BooleanField(default=True,verbose_name="active-user")
    is_admin = models.BooleanField(default=False,verbose_name="admin")
    phone = models.CharField(max_length=50,verbose_name="phone-number", unique=True)
    image = models.ImageField(upload_to = "profiles/images" , blank = True , null = True,verbose_name="user-image")
    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD="email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name="user"
        verbose_name_plural="users"
#--------------------------------------------------------------------------------------------------------------------
class Otp(models.Model):
    token=models.CharField(max_length=32)
    phone=models.CharField(max_length=11)
    code=models.SmallIntegerField()
    expiration_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name="optcode"
        verbose_name_plural="optcodes"


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    full_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=12)
    address=models.CharField(max_length=300)
    postal_code=models.CharField(max_length=30)

    def __str__(self):
        return self.user.phone



    