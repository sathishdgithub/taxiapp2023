from django import forms
from django.forms.widgets import *
from .models import *

class UserForm(forms.Form):
	user_id = forms.CharField(max_length=20)
	access_level = forms.IntegerField()

class AdminLoginForm(forms.Form):
	username 	= forms.EmailField()
	password	= forms.CharField(widget = forms.PasswordInput)

class TaxidetailsForm(forms.ModelForm):

    class Meta:
        model = Taxi_Detail
        fields = ('driver_name', 'address', 'phone_number', 'other_details', 'number_plate')

class TaxisearchForm(forms.Form):
	taxi_id = forms.IntegerField()