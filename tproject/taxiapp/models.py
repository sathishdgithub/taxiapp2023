from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

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



class Taxi_Detail(models.Model):
	number_plate 		= models.CharField(max_length = 20)
	driver_name 		= models.CharField(max_length = 40)
	address 			= models.CharField(max_length = 200)
	phone_number 		= models.IntegerField()
	other_details 		= models.CharField(max_length = 200, blank = True)
	num_of_complaints 	= models.IntegerField()
	driver_image        = models.ImageField(upload_to='drivers',
                              default = 'media/default_qr.png')
	qr_image            = models.ImageField(upload_to='qr',
                              default = 'media/default_qr.png')
	def __str__(self):
		return self.driver_name


class Complaint_Statement(models.Model):
	complaint 			= models.CharField(max_length = 100)

class Admin_Detail(models.Model):
	sms_number			= models.IntegerField()
	whatsapp_number 	= models.IntegerField()
	address				= models.CharField(max_length = 200, blank = True)
	coordinate_x		= models.IntegerField()
	coordinate_y		= models.IntegerField()


class User_Complaint(models.Model):
	user_locations_x 	= models.IntegerField()
	user_locations_y 	= models.IntegerField()
	taxi_id 			= models.ForeignKey('Taxi_Detail', on_delete=models.CASCADE)
	complaint_id		= models.ForeignKey('Complaint_Statement', on_delete=models.CASCADE)
	admin_id 			= models.ForeignKey('Admin_Detail', on_delete=models.CASCADE) 
