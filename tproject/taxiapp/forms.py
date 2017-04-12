from django import forms
from django.forms.widgets import *
from .models import *

class UserForm(forms.Form):
	user_id = forms.CharField(max_length=20)
	access_level = forms.IntegerField()

class AdminLoginForm(forms.Form):
	username 	= forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}), label='')
	password	= forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder' : 'Password'}),  label='')

class TaxidetailsForm(forms.ModelForm):
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate','driver_name','address','city','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver')
    
    def save(self, *args, **kwargs):
        self.instance.traffic_number = self.instance.city.city_code+'-TR-'+str(self.instance.city.taxi_no+1).zfill(5)
        t = City_Code.objects.get(id=self.instance.city.id)
        t.taxi_no = t.taxi_no+1
        t.save()
        return super(TaxidetailsForm, self).save(*args, **kwargs)


class TaxisearchForm(forms.Form):
	taxi_id = forms.IntegerField(widget=forms.TextInput(attrs={'class' : '', 'placeholder' : 'Taxi ID or Auto ID', 'maxlength' : '64'}), label='')

class ComplaintUserForm(forms.ModelForm):
    class Meta:
        model = Complaint_Statement
        fields = ('taxi','reason','city','phone_number','complaint','area')
    def save(self, *args, **kwargs):
        self.instance.complaint_number = self.instance.city.city_code+'-CN-'+str(self.instance.city.complaint_no+1).zfill(7)
        t = City_Code.objects.get(id=self.instance.city.id)
        t.complaint_no = t.complaint_no+1
        t.save()
        return super(ComplaintUserForm, self).save(*args, **kwargs)


           
