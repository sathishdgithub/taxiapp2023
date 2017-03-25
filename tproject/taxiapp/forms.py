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
        fields = ('number_plate','driver_name', 'traffic_number','address','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver')

class TaxisearchForm(forms.Form):
	taxi_id = forms.IntegerField(widget=forms.TextInput(attrs={'class' : '', 'placeholder' : 'Taxi ID', 'maxlength' : '64'}), label='')

class ComplaintUserForm(forms.ModelForm):
    class Meta:
        model = Complaint_Statement
        fields = ('taxi','reason','complaint')

           
