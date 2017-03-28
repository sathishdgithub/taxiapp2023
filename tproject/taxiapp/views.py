from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import *
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys

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
    nex = request.GET.get('next', '')
    print nex
    if request.user.is_authenticated():
    	if request.user.is_admin:
    		return HttpResponseRedirect("/admin")
    	else:
    		return HttpResponseRedirect("/"+nex)
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
                if nex != '':
                    return HttpResponseRedirect("/"+nex)
                else:
                    return HttpResponseRedirect("/drivers_list")
            else:
                return HttpResponse("You're account is disabled.")
        else:
            print  "Invalid Login Details " + username + " " + password
            return render(request, 'taxiapp/admin_login.html', {'form': form,'nex':nex})
    else:
        form = AdminLoginForm()
        return render(request, 'taxiapp/admin_login.html', {'form': form,'nex':nex})

def admin_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

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
            form.save()
            taxi = Taxi_Detail.objects.get(id=form.instance.id)
            taxi.num_of_complaints = 0
            taxi.traffic_number = taxi.traffic_number + str(taxi.id).zfill(5)
            taxi.save()
            return taxi_detail(request, taxi.pk)
    else:
        form = TaxidetailsForm()
    return render(request, 'taxiapp/taxi_edit.html', {'form': form})

def complaint_form(request,pk):
    if request.method == "POST":
        form = ComplaintUserForm(request.POST)
        if form.is_valid():
            form.save()
            t = Taxi_Detail.objects.get(id=form.instance.taxi.id)
            t.num_of_complaints = t.num_of_complaints+1
            t.save()
            return HttpResponseRedirect("/complaint_success/"+str(form.instance.id)) 
    else:
        point = request.GET.get('point','')
        if point != '':
            form = ComplaintUserForm({'taxi':pk,'area':'https://www.google.co.in/maps/@'+point+',16z'})
            form.fields['area'].widget = forms.TextInput(attrs={'size':'200','readonly':"True"})
        else:
            form = ComplaintUserForm({'taxi':pk})
        form.fields['taxi'].widget = forms.TextInput(attrs={'size':'30','readonly':"True"})
    	return render(request, 'taxiapp/complaint.html', {'form': form})

def complaint_success(request,pk):
    return render(request,'taxiapp/complaint_success.html',{'message':'Your complaint for Taxi has been successfully registered. Complaint Number: '+str(pk)})

def complaint_resolve(request,pk):
    if request.user.is_authenticated():
        row = Complaint_Statement.objects.get(id=pk)
        taxi = row.taxi
        t = Taxi_Detail.objects.get(id=taxi.id)
        t.num_of_complaints = max(0,t.num_of_complaints-1)
        t.save()
        row.resolved = True
        row.save()
        return HttpResponseRedirect("/complaint_list") 
    else:
        return HttpResponseRedirect("/admin_login?next=complaint_resolve")

def complaint_list(request):
    if request.user.is_authenticated():
    	rows = Complaint_Statement.objects.all()
    	reasons = Complaint_Statement.REASONS
    	return render(request,'taxiapp/complaint_list.html',{'rows':rows,'reasons':reasons})
    else:
    	return HttpResponseRedirect("/admin_login?next=complaint_list")

def taxi_list(request):
    if request.user.is_authenticated():
        rows = Taxi_Detail.objects.all()
        return render(request,'taxiapp/taxi_list.html',{'rows':rows})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_list")

def get_distance(lat,lon,x,y):
    return (lat-x)**2+(lon-y)**2

def taxi_emergency(request,lat,lon,taxi_id):
    rows = MyUser.objects.all()
    lat,lon = float(lat),float(lon)
    if len(rows) > 0:
        if rows[0].location:
            x,y = map(float,rows[0].location.strip().split(','))
            police,min_distance = rows[0],get_distance(lat,lon,x,y)
        else:
            police,min_distance = rows[0],sys.maxint
        for row in rows:
            if row.location:
                x,y = map(float,row.location.strip().split(','))
                distance = get_distance(lat,lon,x,y)
                if distance < min_distance:
                    min_distance = distance
                    police = row
        return render(request,'taxiapp/taxi_emergency.html',{'message':'', 'distance':min_distance,'police':police})
    else:
        return render(request,'taxiapp/taxi_emergency.html',{'message':'There is no police station nearby.'})
    
