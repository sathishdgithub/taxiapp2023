from django import forms
from django.forms.widgets import *

class UserForm(forms.Form):
	user_id = forms.CharField(max_length=20)
	access_level = forms.IntegerField()

class AdminLoginForm(forms.Form):
	username 	= forms.EmailField()
	password	= forms.CharField(widget = forms.PasswordInput)