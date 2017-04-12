from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
import qrcode
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from location_field.models.plain import PlainLocationField
import StringIO

class City_Code(models.Model):
      city = models.CharField(max_length=40)
      city_code = models.CharField(max_length=10)
      whatsapp = models.BooleanField(default=True)
      sms = models.BooleanField(default=True)
      taxi_no = models.IntegerField(default=0)
      police_no = models.IntegerField(default=0)
      complaint_no = models.IntegerField(default=0)
      def __str__(self):
          return self.city_code+' '+self.city

      class Meta:
          verbose_name = 'City Code'
          verbose_name_plural = 'City Codes'

class MyUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(email,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
        user_number = models.CharField(max_length=20,null=True,blank=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	sms_number = models.IntegerField(null=True)
        area = models.CharField(max_length=200)
	city = models.ForeignKey(City_Code,null=True)
	location = PlainLocationField(based_fields=['area'], zoom=7,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'

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


        class Meta:
                verbose_name = 'Administrator'
                verbose_name_plural = 'Administrators'

class Taxi_Detail(models.Model):
	number_plate = models.CharField(max_length = 20)
	traffic_number = models.CharField(max_length = 20)
	driver_name = models.CharField(max_length = 40)
	son_of = models.CharField(max_length = 40)
	date_of_birth = models.DateField(null=True,blank=True)
	phone_number = models.CharField(max_length=13)
	address = models.CharField(max_length = 200, blank = True)
        city = models.ForeignKey(City_Code)
	aadhar_number = models.CharField(max_length=14,null=True,blank=True)
	driving_license_number = models.CharField(max_length=30,null=True,blank=True)
	date_of_validity = models.DateField(null=True,blank=True)
	autostand = models.CharField(max_length=80,null=True,blank=True)
	union = models.CharField(max_length=100,null=True,blank=True)
	insurance = models.DateField(null=True,blank=True)
	capacity_of_passengers = models.CharField(max_length=10,null=True,blank=True)
	pollution = models.DateField(null=True,blank=True)
	engine_number = models.CharField(max_length=20,null=True,blank=True)
	chasis_number = models.CharField(max_length=20,null=True,blank=True)
	owner_driver = models.CharField(max_length=6,choices=(('Owner','Owner'),('Driver','Driver')),default='Owner',null=True,blank=True)
	num_of_complaints = models.IntegerField(default=0)
	driver_image = models.ImageField(upload_to='drivers',default = 'drivers/profile.png')
	qr_code = models.ImageField(upload_to='qr', blank=True, null=True)
	
	def __str__(self):
		return self.driver_name+'('+self.number_plate+')'

	def generate_qrcode(self):
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=6,
			border=0,
		)
                weburl = "https://taxiapp.safeautotaxi.com/taxi"
		qr.add_data("%s/%s" % (weburl, str(self.traffic_number)))
		qr.make(fit=True)

		img = qr.make_image()

		buffer = StringIO.StringIO()
		img.save(buffer)
		file_name = 'qr-%s.png' % self.pk
		file_buffer = InMemoryUploadedFile(
			buffer, None, file_name, 'image/png', buffer.len, None)
		self.qr_code.save(file_name, file_buffer)

	def save(self, *args, **kwargs):
		add = not self.pk
		super(Taxi_Detail, self).save(*args, **kwargs)

		if add:
			self.generate_qrcode()
			kwargs['force_insert'] = False # create() uses this, which causes error.
                        self.traffic_number = self.city.city_code+'-TR-'+str(self.city.taxi_no+1).zfill(5)	
                        t = City_Code.objects.get(id=self.city.id)
                        t.taxi_no = t.taxi_no+1
                        t.save()
 		        super(Taxi_Detail, self).save(*args, **kwargs)
       
        class Meta:
            verbose_name = 'Taxi Driver'
            verbose_name_plural = 'Taxi Drivers'

class Reasons(models.Model):
      reason = models.CharField(max_length=100)
      def __str__(self):
          return self.reason
      class Meta:
          verbose_name = 'Complaint Reason'
          verbose_name_plural = 'Complaint Reasons'

class Complaint_Statement(models.Model):
        complaint_number             = models.CharField(max_length=20)
        taxi                         = models.ForeignKey(Taxi_Detail,null=True,blank=True)
        reason			     = models.ForeignKey(Reasons,default=1)
        area                         = models.CharField(max_length=200,default='')
        city                         = models.ForeignKey(City_Code,default=1)
 	phone_number                 = models.CharField(max_length=13)
        complaint 		     = models.CharField(max_length = 100,null=True,blank=True)
        assigned_to                  = models.ForeignKey(MyUser,null=True,blank=True)
        resolved		     = models.BooleanField(default=False)
        def __str__(self):
             return str(self.complaint_number)+' '+self.taxi.driver_name+' '+self.reason.reason

        class Meta:
            verbose_name = 'Customer Complaint'
            verbose_name_plural = 'Customer Complaints'

      
