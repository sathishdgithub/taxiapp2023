from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import *
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
	if request.user.is_authenticated():
		return HttpResponse("Hello, you are logged in.")
	else:
		return HttpResponse("Hello, you are logged out.")

def home(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

 
		if form.is_valid():
			user_id = request.POST.get('user_id', '')
			access_level = request.POST.get('access_level', '')
		login_details_obj = Login_Details(user_id=user_id, access_level=access_level)
		login_details_obj.save()
 
		return render(request, 'taxiapp/home.html', {'user_id': user_id,'is_registered':True })
 
	else:
		form = UserForm()
		return render(request, 'taxiapp/home.html', {'form': form})


def admin_login(request):
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
                return HttpResponseRedirect("/drivers_list")
            else:
                return HttpResponse("You're account is disabled.")
        else:
            print  "invalid login details " + username + " " + password
            return render(request, 'taxiapp/admin_login.html', {'form': form})
    else:
        form = AdminLoginForm()
        return render(request, 'taxiapp/admin_login.html', {'form': form})


def drivers_list(request):
    if request.method == "POST":
        form = TaxisearchForm(request.POST)
        taxi_id = request.POST.get('taxi_id', '')
        print taxi_id
        return HttpResponseRedirect("/taxi/"+taxi_id)
    else:
        form = TaxisearchForm()
        return render(request, 'taxiapp/drivers_list.html', {'form' : form})

def taxi_detail(request, pk):
    taxi = get_object_or_404(Taxi_Detail, pk=pk)
    return render(request, 'taxiapp/taxi_detail.html', {'taxi': taxi})

def taxi_new(request):
    if request.method == "POST":
        form = TaxidetailsForm(request.POST)
        if form.is_valid():
            taxi = form.save(commit=False)
            taxi.web_page_url = "/"
            taxi.num_of_complaints = 2
            taxi.save()
            return taxi_detail(request, taxi.pk)
    else:
        form = TaxidetailsForm()
    return render(request, 'taxiapp/taxi_edit.html', {'form': form})
    
