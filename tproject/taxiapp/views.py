from django.shortcuts import render
from django.http import *
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import *
from models import *

def index(request):
	if request.user.is_authenticated():
		return HttpResponse("Hello, you are logged in.")
	else:
		return HttpResponse("Hello, you are logged out.")

def home(request):
	if request.method == 'POST':  # if the form has been filled
		form = UserForm(request.POST)

 
		if form.is_valid():  # All the data is valid
			user_id = request.POST.get('user_id', '')
			access_level = request.POST.get('access_level', '')
        # creating an user object containing all the data
		login_details_obj = Login_Details(user_id=user_id, access_level=access_level)
        # saving all the data in the current object into the database
		login_details_obj.save()
 
		return render(request, 'taxiapp/home.html', {'user_id': user_id,'is_registered':True }) # Redirect after POST
 
	else:
		form = UserForm()  # an unboundform
		return render(request, 'taxiapp/home.html', {'form': form})


def admin_login(request):
    #context = RequestContext(request)
    if request.user.is_authenticated():
    	if request.user.is_admin:
    		return HttpResponseRedirect("/admin")
    	else:
    		return HttpResponseRedirect("/drivers_list")
    if request.method == 'POST':
    	form 	 = AdminLoginForm(request.POST)
    	username = ''
    	password = ''
    	if form.is_valid():
    		username = request.POST.get('username', '')
    		password = request.POST.get('password', '') 

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to index page.
                return HttpResponseRedirect("/drivers_list")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("You're account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print  "invalid login details " + username + " " + password
            return render(request, 'taxiapp/admin_login.html', {'form': form})
    else:
        # the login is a  GET request, so just show the user the login form.
        form = AdminLoginForm()
        return render(request, 'taxiapp/admin_login.html', {'form': form})


def drivers_list(request):
	return render(request, 'taxiapp/drivers_list.html', {})
