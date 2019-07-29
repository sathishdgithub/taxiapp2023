from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
import qrcode
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from location_field.models.plain import PlainLocationField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import StringIO
from werkzeug import secure_filename

class Active(models.Model):
      active_name = models.CharField(max_length=10)

      def __str__(self):
        return self.active_name

      class Meta:
            verbose_name = 'Active Name'
            verbose_name_plural = 'Active Names'      

class Vehicle_type(models.Model):
      
      vehicle_type = models.CharField(max_length=10,unique=True)
      active_id_fk = models.ForeignKey(Active,null=True)
      created_by = models.CharField(max_length=50)
      created_time = models.DateTimeField(auto_now=True)
      modified_by = models.CharField(max_length=50)
      modified_time = models.DateTimeField(auto_now=True)
      
      def __str__(self):
        return self.vehicle_type

      class Meta:
            verbose_name = 'Vehicle type'
            verbose_name_plural = 'Vehicle types'

      

class Owner(models.Model):
      owner_name = models.CharField(max_length = 40, verbose_name="Name")
      address = models.CharField(max_length = 200, blank = True)
      date_of_birth = models.DateField(null=True,blank=True)
      son_of = models.CharField(max_length = 40)
      phone_number = models.CharField(max_length=16)
      aadhar_number = models.CharField(max_length=22,null=True,blank=True)
      owner_image = models.ImageField(upload_to='owners',default = 'owners/profile.png')
      owner_image_thumbnail = ImageSpecField(source='owner_image',
                                      processors=[ResizeToFill(75, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
      owner_image_name = models.CharField(max_length = 100, null=True, blank = True)
      active_id_fk = models.ForeignKey(Active,null=True)
      created_by = models.CharField(max_length=50)
      created_time = models.DateTimeField(auto_now=True)
      modified_by = models.CharField(max_length=50)
      modified_time = models.DateTimeField(auto_now=True)

      def __str__(self):
        return self.owner_name+' '+self.phone_number
      
      class Meta:
            verbose_name = 'Owner'
            verbose_name_plural = 'Owners'

class Vehicle(models.Model):

      traffic_number = models.CharField(max_length = 28,default='',unique=True)
      number_plate = models.CharField(max_length = 24)
      vehicle_type_id_fk = models.ForeignKey(Vehicle_type,null=True)
      owner_id_fk = models.ForeignKey(Owner,null=True)                                                                                                                                                       
      autostand = models.CharField(max_length=80,null=True,blank=True, verbose_name="Stand")
      union = models.CharField(max_length=100,null=True,blank=True)
      #city = models.ForeignKey(City_Code,null=True)
      insurance = models.DateField(null=True,blank=True)
      capacity_of_passengers = models.CharField(max_length=14,null=True,blank=True)
      pollution = models.DateField(null=True,blank=True)
      engine_number = models.CharField(max_length=40,null=True,blank=True)
      chasis_number = models.CharField(max_length=30,null=True,blank=True)
      is_owner_driver = models.CharField(max_length=6,choices=(('OWNER','Owner'),('DRIVER','Driver')),default='OWNER',null=True,blank=True)
      rc_number = models.CharField(max_length = 28,default='')
      rc_expiry = models.DateField(null=True,blank=True)
      active_id_fk = models.ForeignKey(Active,null=True)
      created_by = models.CharField(max_length=50)
      created_time = models.DateTimeField(auto_now=True)
      modified_by = models.CharField(max_length=50)
      modified_time = models.DateTimeField(auto_now=True)
      
      def __str__(self):
        return self.traffic_number+' '+self.number_plate

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
        file_name = secure_filename('%s.png' % self.traffic_number)
        file_buffer = InMemoryUploadedFile(
            buffer, None, file_name, 'image/png', buffer.len, None)
        self.qr_code.save(file_name, file_buffer)

      def save(self, *args, **kwargs):
        add = not self.pk
        super(Vehicle, self).save(*args, **kwargs)

        if add:
			self.generate_qrcode()
			kwargs['force_insert'] = False # create() uses this, which causes error.
                        if self.traffic_number.strip()=='' or self.traffic_number.strip()=='-':
                            self.traffic_number = self.city.city_code+'-TR-'+str(self.city.taxi_no+1).zfill(5)	
                        t = City_Code.objects.get(id=self.city.id)
                        t.taxi_no = t.taxi_no+1
                        t.save()
                        if ' ' in self.number_plate:
                             m = self.number_plate
                             self.number_plate = m.replace(' ','')
 		        super(Vehicle, self).save(*args, **kwargs)
       
        @property
        def get_number_plate(self):
            np = self.number_plate.replace('-','')[:]
            try:
                k = np[0]
                for i in range(1,len(np)):
                    if np[i]=='-':
                        pass
                    elif ((np[i-1].isalpha()) and (np[i].isdigit())) or ((np[i-1].isdigit()) and (np[i].isalpha())):
                        k = k + ' '+np[i]
                    else:
                        k = k + np[i]
                return k
            except Exception as e:
                return self.number_plate

      class Meta:
            verbose_name = 'Vehicle'
            verbose_name_plural = 'Vehicles'

class Driver(models.Model):
      vehicle_id_fk = models.ForeignKey(Vehicle,null=True)
      driver_name = models.CharField(max_length = 40, verbose_name="Name")
      address = models.CharField(max_length = 200, blank = True)
      date_of_birth = models.DateField(null=True,blank=True)
      son_of = models.CharField(max_length = 40)
      phone_number = models.CharField(max_length=16)
      aadhar_number = models.CharField(max_length=22,null=True,blank=True)
      dl_number = models.CharField(max_length=22,null=True,blank=True)
      dl_expiry = models.DateField(null=True,blank=True)
      driver_image = models.ImageField(upload_to='drivers',default = 'drivers/profile.png')
      driver_image_thumbnail = ImageSpecField(source='driver_image',
                                      processors=[ResizeToFill(75, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
      driver_image_name = models.CharField(max_length = 100, null=True, blank = True)
      active_id_fk = models.ForeignKey(Active,null=True)
      created_by = models.CharField(max_length=50)
      created_time = models.DateTimeField(auto_now=True)
      modified_by = models.CharField(max_length=50)
      modified_time = models.DateTimeField(auto_now=True)
      
      def __str__(self):
        return self.driver_name+' '+self.phone_number

      class Meta:
            verbose_name = 'Driver'
            verbose_name_plural = 'Drivers'

class City_Code(models.Model):
      city = models.CharField(max_length=40)
      city_code = models.CharField(max_length=10)
      whatsapp = models.BooleanField(default=True)
      sms = models.BooleanField(default=True)
      distress = models.BooleanField(default=False)
      distress_contact = models.CharField(max_length=13,null=True,blank=True)
      taxi_no = models.BigIntegerField(default=0)
      police_no = models.BigIntegerField(default=0)
      complaint_no = models.BigIntegerField(default=0)
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
                user.is_staff = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
        user_number = models.CharField(max_length=20,null=True,blank=True)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	sms_number = models.BigIntegerField(null=True)
        whatsapp_number = models.BigIntegerField(null=True)
        area = models.CharField(max_length=200)
	city = models.ForeignKey(City_Code,null=True)
	location = PlainLocationField(based_fields=['area'], zoom=7,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False, verbose_name="Admin")
        is_staff = models.BooleanField(default=False, verbose_name="Moderator")

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
        def is_superuser(self):
            "Is the user a member of admin?"
            # Simplest possible answer: All admins are superuser
            return self.is_admin

        class Meta:
                verbose_name = 'Administrator'
                verbose_name_plural = 'Administrators'

class Taxi_Detail(models.Model):
	number_plate = models.CharField(max_length = 24)
	traffic_number = models.CharField(max_length = 28,default='',unique=True)
	driver_name = models.CharField(max_length = 40, verbose_name="Name")
	son_of = models.CharField(max_length = 40)
	date_of_birth = models.DateField(null=True,blank=True)
	phone_number = models.CharField(max_length=16)
	address = models.CharField(max_length = 200, blank = True)
        city = models.ForeignKey(City_Code, related_name='taxidetails')
	aadhar_number = models.CharField(max_length=22,null=True,blank=True)
	driving_license_number = models.CharField(max_length=30,null=True,blank=True)
	date_of_validity = models.DateField(null=True,blank=True)
	autostand = models.CharField(max_length=80,null=True,blank=True, verbose_name="Stand")
	union = models.CharField(max_length=100,null=True,blank=True)
	insurance = models.DateField(null=True,blank=True)
	capacity_of_passengers = models.CharField(max_length=14,null=True,blank=True)
	pollution = models.DateField(null=True,blank=True)
	engine_number = models.CharField(max_length=40,null=True,blank=True)
	chasis_number = models.CharField(max_length=30,null=True,blank=True)
	owner_driver = models.CharField(max_length=6,choices=(('OWNER','Owner'),('DRIVER','Driver')),default='OWNER',null=True,blank=True)
	num_of_complaints = models.BigIntegerField(default=0)
	driver_image = models.ImageField(upload_to='drivers',default = 'drivers/profile.png')
	driver_image_thumbnail = ImageSpecField(source='driver_image',
                                      processors=[ResizeToFill(75, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
        qr_code = models.ImageField(upload_to='qr', blank=True, null=True)
        driver_image_name = models.CharField(max_length = 100, null=True, blank = True)

            
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
		file_name = secure_filename('%s.png' % self.traffic_number)
		file_buffer = InMemoryUploadedFile(
			buffer, None, file_name, 'image/png', buffer.len, None)
		self.qr_code.save(file_name, file_buffer)

	def save(self, *args, **kwargs):
		add = not self.pk
		super(Taxi_Detail, self).save(*args, **kwargs)

		if add:
			self.generate_qrcode()
			kwargs['force_insert'] = False # create() uses this, which causes error.
                        if self.traffic_number.strip()=='' or self.traffic_number.strip()=='-':
                            self.traffic_number = self.city.city_code+'-TR-'+str(self.city.taxi_no+1).zfill(5)	
                        t = City_Code.objects.get(id=self.city.id)
                        t.taxi_no = t.taxi_no+1
                        t.save()
                        if ' ' in self.number_plate:
                             m = self.number_plate
                             self.number_plate = m.replace(' ','')
 		        super(Taxi_Detail, self).save(*args, **kwargs)
       
        @property
        def get_number_plate(self):
            np = self.number_plate.replace('-','')[:]
            try:
                k = np[0]
                for i in range(1,len(np)):
                    if np[i]=='-':
                        pass
                    elif ((np[i-1].isalpha()) and (np[i].isdigit())) or ((np[i-1].isdigit()) and (np[i].isalpha())):
                        k = k + ' '+np[i]
                    else:
                        k = k + np[i]
                return k
            except Exception as e:
                return self.number_plate
        class Meta:
            verbose_name = 'Driver/Owner'
            verbose_name_plural = 'Drivers & Owners'

class Reasons(models.Model):
      reason = models.CharField(max_length=100)
      def __str__(self):
          return self.reason
      class Meta:
          verbose_name = 'Complaint Reason'
          verbose_name_plural = 'Complaint Reasons'

class Complaint_Statement(models.Model):
        complaint_number             = models.CharField(max_length=20)
        taxi                         = models.ForeignKey(Taxi_Detail,null=True,blank=True, verbose_name="Vehicle ID")
        reason			     = models.ForeignKey(Reasons,default=1)
        area                         = models.CharField(max_length=200,default='')
        city                         = models.ForeignKey(City_Code,default=1)
 	origin_area                  = models.CharField(max_length=200,null=True,blank=True)
        destination_area             = models.CharField(max_length=200,null=True,blank=True)
        phone_number                 = models.CharField(max_length=13)
        complaint 		     = models.CharField(max_length = 100,null=True,blank=True)
        assigned_to                  = models.ForeignKey(MyUser,null=True,blank=True)
        resolved		     = models.BooleanField(default=False)
        def __str__(self):
             return str(self.complaint_number)+' '+self.taxi.driver_name+' '+self.reason.reason

        class Meta:
            verbose_name = 'Customer Complaint'
            verbose_name_plural = 'Customer Complaints'

class Otp_Codes(models.Model):
    user = models.ForeignKey(MyUser,null=True,blank=True)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)+" "+str(self.otp)
    class Meta:
        verbose_name = "OTP Code"
        verbose_name_plural = "OTP Codes"
