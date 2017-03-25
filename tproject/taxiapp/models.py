from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
import qrcode
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from location_field.models.plain import PlainLocationField


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
    city = models.CharField(max_length=255,default='Hyderabad')
    location = PlainLocationField(based_fields=['city'], zoom=7,null=True,blank=True)
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
	number_plate = models.CharField(max_length = 20)
        traffic_number = models.CharField(max_length = 20)
	driver_name = models.CharField(max_length = 40)
        son_of = models.CharField(max_length = 40)
	date_of_birth		= models.DateField(null=True,blank=True)
        phone_number 		= models.CharField(max_length=13)
        address 		= models.CharField(max_length = 200, blank = True)
        aadhar_number		= models.CharField(max_length=14)
        driving_license_number  = models.CharField(max_length=30)
        date_of_validity        = models.DateField(null=True,blank=True)
        autostand               = models.CharField(max_length=80)
        union                   = models.CharField(max_length=100)
        insurance               = models.DateField(null=True,blank=True)
        capacity_of_passengers  = models.CharField(max_length=10)
        pollution               = models.DateField(null=True,blank=True)
        engine_number           = models.CharField(max_length=20)
        chasis_number           = models.CharField(max_length=20)
        owner_driver            = models.CharField(max_length=6,choices=(('Owner','Owner'),('Driver','Driver')),default='Owner',)
  	num_of_complaints 	= models.IntegerField(default=0)
	driver_image        = models.ImageField(upload_to='drivers',
                              default = 'media/default_qr.png')
	qrcode            	= models.ImageField(upload_to='qr', blank=True, null=True)
	
	def __str__(self):
		return self.driver_name+'('+self.number_plate+')'
	def generate_qrcode(self):
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=6,
			border=0,
		)
		qr.add_data(self.id)
		qr.make(fit=True)

		img = qr.make_image()

		buffer = StringIO.StringIO()
		img.save(buffer)
		filename = 'qr-%s.png' % (self.id)
		filebuffer = InMemoryUploadedFile(
			buffer, None, filename, 'image/png', buffer.len, None)
		self.qrcode.save(filename, filebuffer)



class Complaint_Statement(models.Model):
        REASONS =  (
        ('R1', 'I was involved in an accident.'),
        ('R2', 'I lost an item.'),
        ('R3', 'I would like a refund.'),
        ('R4', 'My driver was unprofessional'),
	('R5', 'My vehicle was not what I expected.'),
        ('R6', 'I cannot request a ride.'),
        ('R7', 'I have a different issue.'),
    	)
        taxi                         = models.ForeignKey(Taxi_Detail,null=True)
        reason			     = models.CharField(max_length=2,choices=REASONS,default='R1',)
	complaint 		     = models.CharField(max_length = 100)
        resolved		     = models.BooleanField(default=False)
        def __str__(self):
             return self.taxi.driver_name+' '+self.reason

class Admin_Detail(models.Model):
	sms_number			= models.IntegerField()
	whatsapp_number 	= models.IntegerField()
	address				= models.CharField(max_length = 200, blank = True)
	coordinate_x		= models.IntegerField()
	coordinate_y		= models.IntegerField()
        city = models.CharField(max_length=255,default='Hyderabad')
        location = PlainLocationField(based_fields=['city'], zoom=7,null=True,blank=True)


class User_Complaint(models.Model):
	user_locations_x 	= models.IntegerField()
	user_locations_y 	= models.IntegerField()
	taxi_id 		= models.ForeignKey(Taxi_Detail, on_delete=models.CASCADE)
	complaint_id		= models.ForeignKey(Complaint_Statement, on_delete=models.CASCADE)
	admin_id 		= models.ForeignKey(Admin_Detail, on_delete=models.CASCADE) 
