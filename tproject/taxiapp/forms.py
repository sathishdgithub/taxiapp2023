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
        fields = ('driver_name', 'address', 'phone_number', 'other_details', 'number_plate')

class TaxisearchForm(forms.Form):
	taxi_id = forms.IntegerField(widget=forms.TextInput(attrs={'class' : '', 'placeholder' : 'Taxi ID', 'maxlength' : '64'}), label='')

class ComplaintUserForm(forms.ModelForm):
    class Meta:
        model = Complaint_Statement
        fields = ('taxi','reason','complaint')

           
