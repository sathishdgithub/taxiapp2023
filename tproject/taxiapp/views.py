from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.contrib.auth.views import password_change
from forms import *
from models import *
import urllib2, simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import sys
import requests
from django.views.decorators.csrf import csrf_exempt
from urlparse import urlparse
from whatsapp import Client
import pandas as pd
import random,datetime
from rest_framework import viewsets
from rest_framework.views import APIView
from serializers import TaxiDriverOwnerSerialize
from serializers import TaxiComplaintsSerialize
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from collections import OrderedDict
from rest_framework.filters import BaseFilterBackend
import coreapi
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO
from . import constants
import urllib,shutil,os,zipfile
from datetime import date, tzinfo, datetime, timedelta
 



client = Client(login='919704807427', password='CM3u2jJb7sf6leMmQdkHJF/xvxI=')

def index(request):
	if request.user.is_authenticated():
		return HttpResponse("Hello, you are logged in.")
	else:
		return HttpResponse("Hello, you are logged out.")


def strip_scheme(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)

def googl(url):
    """ Code : Using Cutly Acccess Token """
    req = urllib2.Request(constants.CUTLY_API+'?key='+constants.CUTLY_ACCESS_TOKEN+'&short='+url)
    f = urllib2.urlopen(req)
    resJson = (simplejson.loads(f.read())['url'])
    return resJson['shortLink']
    """ Code : Using Cutly Acccess Token """


def home(request):
    if request.method == "POST":
        form = TaxisearchForm(request.POST)
        taxi_id = request.POST.get('taxi_id', '')
        print taxi_id
        return HttpResponseRedirect("/taxi/"+taxi_id)
    else:
        form = TaxisearchForm()
        message = request.GET.get('message','')
        return render(request, 'taxiapp/drivers_list.html', {'form' : form, 'message': message})



def admin_login(request):
    nex = request.GET.get('next', 'taxi_list')
    if request.user.is_authenticated():
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
                    return HttpResponseRedirect("/")
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

def administrator(request):
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

def taxi_detail(request, pk):
    if ' ' in pk:
        pk = pk.replace(' ','')

    drivers = []
    vehicle = Vehicle()
    owner = Owner()
    vehicles = Vehicle.objects.filter(traffic_number__iexact = pk)
    if(len(vehicles) == 0):
       vehicles = Vehicle.objects.filter(number_plate__iexact = pk)
    if(len(vehicles) == 0):
        drivers = Driver.objects.filter(traffic_number__iexact = pk)
        if len(drivers) > 0:
            driver = drivers[0]
            vehicle = Vehicle.objects.get(id = driver.vehicle.id)
            owner = vehicle.owner
    if(vehicle.id is None and len(vehicles) > 0):
        vehicle = vehicles[0]
        owner = vehicle.owner
    if(len(drivers) == 0 and vehicle.id is not None):
        drivers = Driver.objects.filter(vehicle = vehicle)
    
    for driver in drivers:
        if (driver is not None):
            bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
            s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            bucket = s3.Bucket(bucketName)   
            try:                                
                fileName = str(driver.driver_image)
                objs = list(bucket.objects.filter(Prefix=fileName))
                if(len(objs) == 0):
                    driver.driver_image = 'images/profile.png'
            except Exception as e:
                driver.driver_image = 'images/profile.png'
                #print(e)

    if (vehicle.id is not None):
        m = vehicle
        k,p = m.number_plate,''
        k.replace('-','')
        start,p = k[0],k[0]
        for i in range(1,len(k)):
            if k[i] == '-':
                pass
            elif ((k[i-1].isalpha()) and (k[i].isdigit())) or ((k[i-1].isdigit()) and (k[i].isalpha())):
                p = p+' '+k[i]
            else:
                p = p+k[i]
        m.number_plate = p

    if (owner is not None):
        bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
        s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.Bucket(bucketName)   
        try:                                
            fileName = str(owner.owner_image)
            objs = list(bucket.objects.filter(Prefix=fileName))
            if(len(objs) == 0):
                owner.owner_image = 'images/profile.png'
        except Exception as e:
            owner.owner_image = 'images/profile.png'
            #print(e)
    if(vehicle.id is not None) :
        return render(request, 'taxiapp/taxi_detail.html', {'vehicle': vehicle,'owner':owner,'drivers':drivers}) 
    else:
        return render(request, 'taxiapp/taxi_detail_fail.html', {'message':"No taxis with the given Traffic Number or Number Plate found."})

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

def complaint_form(request):
    if request.method == "POST":
        form = ComplaintUserForm(request.POST)
        if form.is_valid():            
            form.save()
            t = Vehicle.objects.get(id=form.instance.vehicle.id)
            t.num_of_complaints = t.num_of_complaints+1
            t.save()
            return HttpResponseRedirect("/complaint_success/"+str(form.instance.complaint_number))
    else:
        vehicle_id = request.GET.get('id', '')
        passenger_phone = request.GET.get('passenger_phone','')
        passenger_origin = request.GET.get('passenger_origin','')
        passenger_destination = request.GET.get('passenger_destination','')
        form = ComplaintUserForm(initial={'vehicle':vehicle_id,'phone_number':passenger_phone,\
               'origin_area':passenger_origin,'destination_area':passenger_destination})
        form.fields['vehicle'].widget = forms.TextInput(attrs={'size':'30','readonly':"True"})
    	return render(request, 'taxiapp/complaint.html', {'form': form})


def send_sms(message,phone_number,kind):
    if kind == 'emergency':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_FROM_FOR_EMERGENCY,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE}) 
    elif kind == 'complaint':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_FROM_FOR_COMPLAINT,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE})
    elif kind == 'otp':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_FROM_FOR_OTP,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE})
    return r

def send_whatsapp(message,phone_number):
    k = client.send_message('91'+str(phone_number), message=message)
    print message,k
    return k 

def complaint_success(request,pk):
    rows = MyUser.objects.all()
    complaint = Complaint_Statement.objects.get(complaint_number=pk.upper())
    area = complaint.area
    if area.startswith('https://www.google.co.in/maps/place/'):
        lat,lon = map(float,area[len('https://www.google.co.in/maps/place/'):].split(','))
    else:
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+str(area)+"&key=AIzaSyBX_xC2Jeti6f0v83GVrnzX0mvfDyZE9yc")
        m = r.json()["results"][0]["geometry"]["location"]
        lat,lon = float(m["lat"]),float(m["lng"])
    if len(rows) > 0:
        if rows[0].location and (not rows[0].is_admin):
            x,y = map(float,rows[0].location.strip().split(','))
            police,min_distance = rows[0],get_distance(lat,lon,x,y)
        else:
            police,min_distance = rows[0],sys.maxint
        for row in rows:
            if row.location and (not row.is_admin):
                x,y = map(float,row.location.strip().split(','))
                distance = get_distance(lat,lon,x,y)
                if distance < min_distance:
                    min_distance = distance
                    police = row
        phone_number = police.sms_number
        whatsapp_number = police.whatsapp_number
        complaint.assigned_to = police
        complaint.created_time = datetime.now().date()
        complaint.save()
        #taxi = Taxi_Detail.objects.get(id=complaint.taxi.id)
        vehicleObj = Vehicle.objects.get(id=complaint.vehicle.id)
        driver = Driver()
        try:        
            driver = Driver.objects.get(vehicle = vehicleObj)
        except Exception as e:
            print(e.message)
        map_url = 'https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''
        message = 'Complaint\n'+'Name: '+str(driver.driver_name)+'\n'+'Taxi Number: '+str(vehicleObj.number_plate)+'\n'+'Phone Number: '+str(driver.phone_number)+'\nComplaint Reason: '+str(complaint.complaint)+'\nLocation: '+googl(map_url)+'\nPassenger Phone Number: '+str(complaint.phone_number)+'\nOrigin: '+str(complaint.origin_area)+'\nDestination: '+str(complaint.destination_area)
        message1 = 'Your Complaint has been registered.\n'+'Taxi Number: '+str(vehicleObj.number_plate)+'\n'+'Driver Name: '+str(driver.driver_name)+'\nDriver Phone Number: '+str(driver.phone_number)
        if vehicleObj.city.sms:
            m = send_sms(message,phone_number,'complaint')
            n = send_sms(message1,complaint.phone_number,'complaint')
        if vehicleObj.city.whatsapp:
            m = send_whatsapp(message,whatsapp_number)
    return render(request,'taxiapp/complaint_success.html',{'message1':'Your complaint for Taxi has been successfully registered.','message2':'Complaint Number: '+str(pk)})

def complaint_resolve(request):
    if request.user.is_authenticated():
        message = request.GET.get('message')
        complaintId = request.GET.get('id')
        complaintStatement = Complaint_Statement.objects.get(id=complaintId)
        complaintStatement.message = message
        complaintStatement.resolved = True
        complaintStatement.resolved_time = datetime.now().date()
        complaintStatement.save()
        
        resolved_date = complaintStatement.resolved_time
        resolved_date.strftime('%m-%d-%y %H:%M:%S')
        
        print(resolved_date)
        smsMessage = 'Complaint Resolved.\n'+'Taxi Number: '+str(complaintStatement.vehicle.number_plate)+'\nDate: '+str(resolved_date)+'\nComplaint Reason: '+str(complaintStatement.reason.reason)+'\nResolution: '+str(message)

        print(smsMessage)
        print(complaintStatement.phone_number)
        m = send_sms(smsMessage,str(complaintStatement.phone_number),'complaint')
        return HttpResponseRedirect("/taxi_list") 
    else:
        return HttpResponseRedirect("/admin_login?next=complaint_resolve")

def complaint_list(request):
    if request.user.is_authenticated():
    	rows = Complaint_Statement.objects.all()
    	return render(request,'taxiapp/complaint_list.html',{'rows':rows})
    else:
    	return HttpResponseRedirect("/admin_login?next=complaint_list")

def complaint_view(request,pk):
    if request.user.is_authenticated():
        pk = pk.upper()
        row = get_object_or_404(Complaint_Statement, complaint_number=pk)
        if row.vehicle is not None :
            vehicleObj = Vehicle.objects.get(id=row.vehicle.id)
            driver = Driver()
            try :
                driver = Driver.objects.get(vehicle = vehicleObj)
            except Exception as e:
                print(e.message)
            reason_statement = ''

            return render(request,'taxiapp/complaint_view.html',{'row':row,'driver':driver})
        else :
            return render(request,'taxiapp/complaint_view.html',{'row':row})
    else:
        return HttpResponseRedirect("/admin_login?next=complaint_view/"+str(pk))

def taxi_list(request):
    page = 1
    if request.method == "GET":
        page = request.GET.get('page', 1)
    else:
        page = request.POST.get('page', 1)
    #cities = City_Code.objects.order_by('city').values_list('city',flat=True).distinct()
    cities = City_Code.objects.all()
    vehicletypes = Vehicle_type.objects.order_by('vehicle_type').values_list('vehicle_type',flat=True).distinct()
    #vehicletypes = Vehicle_type.objects.all()
    
    if request.user.is_authenticated():
        city_code = None
        city = None
        vehicletype = request.POST.get('vehicletype')
        rangeFrom = request.POST.get('rangeFrom')# Last five digits of Traffic Number
        rangeTo = request.POST.get('rangeTo') # Last five digits of Traffic Number
        taxiIds = request.POST.get('taxiIds') # Traffic Numbers
        numberPlates = request.POST.get('numberPlates') # Number Plates
        if request.user.is_admin:
            city_code = request.POST.get('city_code')
            if(city_code is not None and city_code != 'All'):
                city = City_Code.objects.get(city_code = city_code)
            else :
                city_code = 'All'
        else:
           city = request.user.city
           city_code = city.city_code
        
        if (city_code == 'All') :
            rows = Vehicle.objects.select_related()
            rows_c = Complaint_Statement.objects.select_related('vehicle')
            ratings = Customer_Rating.objects.select_related('vehicle')
            vehicleregistrations = Vehicle_Registration.objects.all()
            dashboardDict = getDashboardData(None)
        else :
            #city = City_Code.objects.get(city_code = city_code)
            rows = Vehicle.objects.select_related().filter(city = city)
            rows_c = Complaint_Statement.objects.filter(city=city)
            ratings = Customer_Rating.objects.filter(vehicle__city = city)
            vehicleregistrations = Vehicle_Registration.objects.select_related().filter(city = city)
            dashboardDict = getDashboardData(city)


        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            rows = rows.filter(vehicle_type=vehicle_type)
            rows_c = rows_c.filter(vehicle__vehicle_type=vehicle_type)
            ratings = ratings.filter(vehicle__vehicle_type=vehicle_type)
            vehicleregistrations=vehicleregistrations.filter(vehicle_type=vehicle_type)
            # dashboardDict = getDashboardData(city)
            todayVR = dashboardDict['todayVR']
            todayVR = todayVR.filter(vehicle_type=vehicle_type)
            dashboardDict.update(todayVR= todayVR)

            thisWeekVR = dashboardDict['thisWeekVR']
            thisWeekVR = thisWeekVR.filter(vehicle_type=vehicle_type)
            dashboardDict.update(thisWeekVR= thisWeekVR)

            thisMonthVR = dashboardDict['thisMonthVR']
            thisMonthVR = thisMonthVR.filter(vehicle_type=vehicle_type)
            dashboardDict.update(thisMonthVR= thisMonthVR)

            thisYearVR = dashboardDict['thisYearVR']
            thisYearVR = thisYearVR.filter(vehicle_type=vehicle_type)
            dashboardDict.update(thisYearVR= thisYearVR)

        else :
            vehicletype = 'All'   
        if (rangeFrom is not None and  rangeFrom != '' and rangeTo is not None and rangeTo != ''):
            rangeFromList = rangeFrom.split('-')
            print(rangeFromList)
            commonStr = rangeFromList[0]+"-"+rangeFromList[1]
            rangeLen = len(rangeFromList[2])
            rangeFromValue = int(rangeFromList[2])
            rangeDiff = ( int(rangeTo.split('-')[2]) - rangeFromValue ) + 1
            rangeList = []            
            for i in range(rangeDiff):
                rangFromValuelen = len(str(rangeFromValue))
                leadingZero = rangeLen - rangFromValuelen
                rangeList.append(commonStr+"-"+str(rangeFromValue).zfill(leadingZero + rangFromValuelen))
                rangeFromValue =  rangeFromValue + 1
            print(rangeList)
            # vehicleDetails = vehicleDetails.filter(traffic_number__in = rangeList)
            rows = rows.filter(traffic_number__in = rangeList)
            rows_c=rows_c.filter(vehicle__traffic_number__in = rangeList)
            ratings=ratings.filter(vehicle__traffic_number__in = rangeList)
            vehicleregistrations=vehicleregistrations.filter(traffic_number__in = rangeList)
            # dashboardDict = getDashboardData(city)
            todayVR = dashboardDict['todayVR']
            todayVR = todayVR.filter(traffic_number__in = rangeList)
            dashboardDict.update(todayVR= todayVR)

            thisWeekVR = dashboardDict['thisWeekVR']
            thisWeekVR = thisWeekVR.filter(traffic_number__in = rangeList)
            dashboardDict.update(thisWeekVR= thisWeekVR)

            thisMonthVR = dashboardDict['thisMonthVR']
            thisMonthVR = thisMonthVR.filter(traffic_number__in = rangeList)
            dashboardDict.update(thisMonthVR= thisMonthVR)

            thisYearVR = dashboardDict['thisYearVR']
            thisYearVR = thisYearVR.filter(traffic_number__in = rangeList)
            dashboardDict.update(thisYearVR= thisYearVR)
        else :
            rangeFrom = ""
            rangeTo = ""
        if (taxiIds is not None and taxiIds != ''):
            taxiIdsArray = taxiIds.split(',')
            rows = rows.filter(traffic_number__in = taxiIdsArray)
            rows_c=rows_c.filter(vehicle__traffic_number__in = taxiIdsArray)
            ratings=ratings.filter(vehicle__traffic_number__in = taxiIdsArray)
            vehicleregistrations=vehicleregistrations.filter(traffic_number__in = taxiIdsArray)
            
            todayVR = dashboardDict['todayVR']
            todayVR = todayVR.filter(traffic_number__in = taxiIdsArray)
            dashboardDict.update(todayVR= todayVR)

            thisWeekVR = dashboardDict['thisWeekVR']
            thisWeekVR = thisWeekVR.filter(traffic_number__in = taxiIdsArray)
            dashboardDict.update(thisWeekVR= thisWeekVR)

            thisMonthVR = dashboardDict['thisMonthVR']
            thisMonthVR = thisMonthVR.filter(traffic_number__in = taxiIdsArray)
            dashboardDict.update(thisMonthVR= thisMonthVR)

            thisYearVR = dashboardDict['thisYearVR']
            thisYearVR = thisYearVR.filter(traffic_number__in = taxiIdsArray)
            dashboardDict.update(thisYearVR= thisYearVR)
        else :
            taxiIds = ""
        if (numberPlates is not None and numberPlates != ''):
            numberPlatesArray = numberPlates.split(',')
            rows = rows.filter(number_plate__in = numberPlatesArray)
            rows_c=rows_c.filter(vehicle__number_plate__in = numberPlatesArray)
            ratings=ratings.filter(vehicle__number_plate__in = numberPlatesArray)
            vehicleregistrations=vehicleregistrations.filter(number_plate__in = numberPlatesArray)
           
            todayVR = dashboardDict['todayVR']
            todayVR = todayVR.filter(number_plate__in = numberPlatesArray)
            dashboardDict.update(todayVR= todayVR)

            thisWeekVR = dashboardDict['thisWeekVR']
            thisWeekVR = thisWeekVR.filter(number_plate__in = numberPlatesArray)
            dashboardDict.update(thisWeekVR= thisWeekVR)

            thisMonthVR = dashboardDict['thisMonthVR']
            thisMonthVR = thisMonthVR.filter(number_plate__in = numberPlatesArray)
            dashboardDict.update(thisMonthVR= thisMonthVR)

            thisYearVR = dashboardDict['thisYearVR']
            thisYearVR = thisYearVR.filter(number_plate__in = numberPlatesArray)
            dashboardDict.update(thisYearVR= thisYearVR)
        else :
            numberPlates = ""

        todayVR = dashboardDict['todayVR']
        dashboardDict.update(todayVR= len(todayVR))

        thisWeekVR = dashboardDict['thisWeekVR']
        dashboardDict.update(thisWeekVR= len(thisWeekVR))

        thisMonthVR = dashboardDict['thisMonthVR']
        dashboardDict.update(thisMonthVR= len(thisMonthVR))

        thisYearVR = dashboardDict['thisYearVR']
        dashboardDict.update(thisYearVR= len(thisYearVR))

        total = len ( Vehicle.objects.all())
        dashboardDict.update(total = total)

        #print(dashboardDict)
        paginator = Paginator(rows, 10)            
        try:
            rowPages = paginator.page(page)
        except PageNotAnInteger:
            rowPages = paginator.page(1)
        except EmptyPage:
            rowPages = paginator.page(paginator.num_pages)
        return render(request,'taxiapp/taxi_list.html',{'rows_c':rows_c,'rows':rowPages,'ratings':ratings,
        'cities':cities,'vehicletypes':vehicletypes,'dashboardDict':dashboardDict, 
        'vehicletype':vehicletype,'rangeFrom':rangeFrom,'city_code':city_code,'numberPlates':numberPlates,
        'vehicleregistrations':vehicleregistrations,'rangeTo':rangeTo,'taxiIds':taxiIds})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_list")

def getDashboardData(city):
    dashboardDict = {}
    if(city is not None):
        # To get today registration count
        timestamp_from = datetime.now().date() - timedelta(days=1)
        timestamp_to = datetime.now().date()
        todayVR = Vehicle.objects.filter(city = city, created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        dashboardDict.update(todayVR = todayVR)
        # To get last 1 week registration count
        timestamp_from = datetime.now().date() - timedelta(days=7)
        timestamp_to = datetime.now().date()
        thisWeekVR = Vehicle.objects.filter(city = city, created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        dashboardDict.update(thisWeekVR = thisWeekVR)
        # To get last 1 month registration count
        timestamp_from = datetime.now().date() - timedelta(days=30)
        timestamp_to = datetime.now().date()
        thisMonthVR = Vehicle.objects.filter(city = city, created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        dashboardDict.update(thisMonthVR = thisMonthVR)
        # To get last 1 year registration count
        timestamp_from = datetime.now().date() - timedelta(days=365)
        timestamp_to = datetime.now().date()
        thisYearVR = Vehicle.objects.filter(city = city, created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        dashboardDict.update(thisYearVR = thisYearVR)
        # To get total count of records
        # total = len ( Vehicle.objects.all())
        # dashboardDict.update(total = total)
    else:
        # To get today registration count
        timestamp_from = datetime.now().date() - timedelta(days=1)
        timestamp_to = datetime.now().date()
        todayVR = Vehicle.objects.filter(created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        #todayVRCount = len(todayVR)
        dashboardDict.update(todayVR = todayVR)
        # To get last 1 week registration count
        timestamp_from = datetime.now().date() - timedelta(days=7)
        timestamp_to = datetime.now().date()
        thisWeekVR = Vehicle.objects.filter(created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        #thisWeekVRCount = len(thisWeekVR)
        dashboardDict.update(thisWeekVR = thisWeekVR)
        # To get last 1 month registration count
        timestamp_from = datetime.now().date() - timedelta(days=30)
        timestamp_to = datetime.now().date()
        thisMonthVR = Vehicle.objects.filter(created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        #thisMonthVRCount = len(thisMonthVR)
        dashboardDict.update(thisMonthVR = thisMonthVR)
        # To get last 1 year registration count
        timestamp_from = datetime.now().date() - timedelta(days=365)
        timestamp_to = datetime.now().date()
        thisYearVR = Vehicle.objects.filter(created_time__gte = timestamp_from,created_time__lt = timestamp_to).distinct() 
        #thisYearVRCount = len(thisYearVR)
        dashboardDict.update(thisYearVR = thisYearVR)
        # To get total count of records
        # total = len ( Vehicle.objects.all())
        # dashboardDict.update(total = total)
    return dashboardDict

def get_distance(lat,lon,x,y):
    return (lat-x)**2+(lon-y)**2

def taxi_emergency(request):
    if request.method == "POST":
        rows = MyUser.objects.all()
        point = request.POST.get('point','0,0')
        vehicle_id = request.POST.get('id')
        p_phone = request.POST.get('passenger_phone_sos','')
        p_origin = request.POST.get('passenger_origin_sos','')       
        p_destination = request.POST.get('passenger_destination_sos','')       
        lat,lon = map(float,point.split(','))
        if len(rows) > 0:
            if rows[0].location and (not rows[0].is_admin):
                x,y = map(float,rows[0].location.strip().split(','))
                police,min_distance = rows[0],get_distance(lat,lon,x,y)
            else:
                police,min_distance = rows[0],sys.maxint
            for row in rows:
                if row.location and (not row.is_admin):
                    x,y = map(float,row.location.strip().split(','))
                    distance = get_distance(lat,lon,x,y)
                    if distance < min_distance:
                        min_distance = distance
                        police = row
            phone_number = police.sms_number
            whatsapp_number = police.whatsapp_number
            vehicle = Vehicle.objects.get(id=vehicle_id)
            driver = Driver()
            try:
                driver = Driver.objects.get(vehicle=vehicle)
            except Exception as e:
                print(e.message)

            """Code to save Emergency Text data into complaints table"""
            area = 'https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)
            city = City_Code.objects.get(pk=police.city.id)
            cs = Complaint_Statement()
            cs.vehicle = vehicle 
            cs.city = city
            cs.area = area
            cs.origin_area = p_origin
            cs.destination_area = p_destination
            cs.phone_number = p_phone
            cs.assigned_to = police
            cs.resolved = False
            cs.is_emergency_text = True 
            cs.complaint_number = city.city_code+'-CN-'+str(city.complaint_no+1).zfill(7)
            cs.save()

            city.complaint_no = city.complaint_no+1
            city.save()

            
            message = 'SOS\n'+'Name: '+str(driver.driver_name)+'\n'+'Taxi Number: '+str(vehicle.number_plate)+'\n'+'Driver Phone Number:'+str(driver.phone_number)+'\nEmergency SOS\nLocation: '+str(googl('https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''))+'\nPassenger Phone Number:'+str(p_phone)+'\nOrigin:'+str(p_origin)+'\nDestination:'+str(p_destination)
            message1 = 'Your SOS has been registered.\n'+'Taxi Number: '+str(vehicle.number_plate)+'\n'+'Driver Name: '+str(driver.driver_name)+'\nDriver Phone Number: '+str(driver.phone_number)
            if vehicle.city.sms:
                m = send_sms(message,phone_number,'emergency')
                n = send_sms(message1,p_phone,'emergency')
            if vehicle.city.whatsapp:
                m = send_whatsapp(message,whatsapp_number)
            return render(request,'taxiapp/taxi_emergency.html',{'message':'', 'distance':min_distance,'police':police})
        else:
            return render(request,'taxiapp/taxi_emergency.html',{'message':'There is no police station nearby.'})
    else:
            return render(request,'taxiapp/error.html')

def date_form(date):                                   
    t = str(date).strip().split('/')                                              
    if len(t) == 3:                               
        d,m,y = t                                                                                                                              
        if (len(y)==4) and (int(m)<=12 and int(m)>=1):                                                                                         
            return y+'-'+m+'-'+d                                                                                                               
        elif (len(y)==4) and (int(d)<=12 and int(d)>=1):                                                                                                          return y+'-'+d+'-'+m                                                             
    return None

def convertToDate(datestr):
    date = None
    if(datestr is not None and datestr != '' and datestr != '-'):
        date = pd.to_datetime(datestr).strftime('%Y-%m-%d')
    return date

def handle_taxi_xls(file_path,city):
    import os,numpy as np
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    owner_vehicle_headers = ['Owner Image Name (30)','Vehicle Number (12)','Traffic Number (13)','Owner Name (40)','Father Name (40)','DOB (DD/MM/YYYY)','ADDRESS (200)','Phone (10)','Aadhaar (12)','DL Number (20)','DL Expiry (DD/MM/YYYY)','Blood Group (3)','Vehicle Make (20)','Vehicle Model (20)','Capacity (2)','Mfg Date (DD/MM/YYYY)','RC Expiry (DD/MM/YYYY)','Engine Number (20)','Chassis Number (25)','Insurance provider (20)','Insurance number (30)','Insurance Date (DD/MM/YYYY)','Auto Stand (40)','Union (40)','Pollution (DD/MM/YYYY)']
    driver_headers = ['Driver Image Name (30)','Vehicle Number (12)','Driver Name (40)','Father Name (40)','DOB (DD/MM/YYYY)','Address (200)','Phone (10)','Aadhaar (12)','DL Number (20)','DL Expiry (DD/MM/YYYY)','Blood Group (3)']

    #Code to upload to s3 Bucket
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        s3.Bucket(bucketName).put_object(Key=file_path.name,Body=file_path)
    except Exception as e:
        return ["network_error"]
          
    all_errors=[]
    try:
        s3_object = s3.Object(bucket_name=bucketName, key=file_path.name)
        owner_vehicle_df = pd.read_exce(s3_object.get()['Body'],sheetname="Vehicle_Owner")
        driver_df = pd.read_excel(s3_object.get()['Body'],sheetname="Driver")
        owner_vehicle_data = owner_vehicle_df.replace(np.nan, '', regex=True)
        driver_data = driver_df.replace(np.nan, '', regex=True)
        if ( len(owner_vehicle_headers) == len(owner_vehicle_data.columns) and len(driver_headers) == len(driver_data.columns)) :
            for ov_column,dvr_column in zip(owner_vehicle_data.columns,driver_data.columns):
                if ( ov_column not in owner_vehicle_headers or dvr_column not in driver_headers ):
                    print(ov_column,dvr_column)
                    s3_object.delete()
                    return ["csv_header_error"]
        else :
            s3_object.delete()
            return ["csv_header_error"]
    except Exception as e:
        print(e.message)
        s3_object.delete()
        return ["csv_file_error"]

    """code to insert First Sheet named - Vehicle_Owner  into Vehicle and Owner Tables"""
    rowNumber = 1
    for index,row in owner_vehicle_data.iterrows(): 
        rowNumber+=1
        try:                                                                          
            c = City_Code.objects.get(pk=city)
            if (len(row["Traffic Number (13)"]) > 3) or (row["Traffic Number (13)"] in ['','-']):
                active = Active.objects.get(active_name = "active") 
                owner = Owner(owner_name=row["Owner Name (40)"],address=row["ADDRESS (200)"],date_of_birth=convertToDate(row["DOB (DD/MM/YYYY)"]),son_of=row['Father Name (40)'],phone_number=row['Phone (10)'],aadhar_number=row['Aadhaar (12)'],owner_image_name=row["Owner Image Name (30)"],blood_group=row["Blood Group (3)"],dl_number = row["DL Number (20)"],dl_expiry= convertToDate(row["DL Expiry (DD/MM/YYYY)"]),active = active)
                owner.save()   
                vehicle = Vehicle(number_plate=row["Vehicle Number (12)"],traffic_number=row["Traffic Number (13)"],vehicle_make=row["Vehicle Make (20)"],vehicle_model=row["Vehicle Model (20)"],insurance = convertToDate(row["Insurance Date (DD/MM/YYYY)"]),insurance_provider=row["Insurance provider (20)"], insurance_number=row["Insurance number (30)"],autostand=row["Auto Stand (40)"],union=row["Union (40)"],capacity_of_passengers=row["Capacity (2)"],pollution=convertToDate(row["Pollution (DD/MM/YYYY)"]),engine_number=row["Engine Number (20)"],chasis_number=row["Chassis Number (25)"],mfg_date=convertToDate(row["Mfg Date (DD/MM/YYYY)"]),rc_expiry=convertToDate(row["RC Expiry (DD/MM/YYYY)"]),city=c,owner = owner)
                vehicle.save()
                
        except Exception as e:
            print(e.message)
            all_errors.append(rowNumber)
            s3_object.delete()
            return all_errors

    """code to insert Second Sheet named - Driver  into Driver Table"""
    rowNumber = 1
    for index,row in driver_data.iterrows(): 
        rowNumber+=1
        try:                                                                          
            if (len(row["Vehicle Number (12)"]) > 3) or (row["Vehicle Number (12)"] in ['','-']):
                
                number_plate = row["Vehicle Number (12)"]
                if ' ' in number_plate:
                    number_plate = number_plate.replace(' ','')
              
                vehicle = Vehicle.objects.get(number_plate = number_plate)
                active = Active.objects.get(active_name = "active")
                d = Driver(driver_name = row['Driver Name (40)'],address=row['Address (200)'],date_of_birth = convertToDate(row['DOB (DD/MM/YYYY)']),son_of = row['Father Name (40)'],phone_number=row['Phone (10)'], aadhar_number = row['Aadhaar (12)'],dl_number=row['DL Number (20)'],dl_expiry = convertToDate(row['DL Expiry (DD/MM/YYYY)']),driver_image=row['Driver Image Name (30)'],vehicle=vehicle,blood_group=row["Blood Group (3)"],active=active)
                d.save()
        except Exception as e:
            print(e.message)
            all_errors.append(rowNumber)
            s3_object.delete()
            return all_errors

    s3_object.delete()
    return all_errors

def handle_bulk_image_zip(file_path):

    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    extension = ".zip"
    all_errors = []
    temp_path = 'temp_bulk_image_upload/'+file_path.name
    #Code to upload to s3 Bucket
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        s3.Bucket(bucketName).put_object(Key=temp_path,Body=file_path)
    except Exception as e:
        all_errors.append(e)
        return ["network_error"]
    
    try:
        item = s3.Object(bucket_name=bucketName, key=temp_path)
        all_errors = unzipAttachment(temp_path, file_path.name)

    except Exception as e:
        print(e.message)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.')
        raise e 
        return(e)
        all_errors.append(e)    
    return all_errors

def unzipAttachment(s3_path,filename):
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    tmpFolder = '/tmp/'
    unzipTmpFile = filename
    extension = ".zip" 
    path = os.getcwd()
    all_errors=[]
   
    if not os.path.exists(tmpFolder):
         os.mkdir(tmpFolder)
    
    if not os.path.exists(tmpFolder+unzipTmpFile):
        try: 
            #os.remove(tmpFolder+unzipTmpFile)
            s3.Bucket(bucketName).download_file(s3_path, tmpFolder+unzipTmpFile)
            os.chdir(tmpFolder)
            for item in os.listdir(tmpFolder):
                if item.endswith(extension): 
                    file_name = os.path.abspath(item)
                    #print(file_name)
                    zip_ref = zipfile.ZipFile(file_name) 
                    zip_ref.extractall(tmpFolder) 
                    zip_ref.close()
                    os.remove(file_name)
            #shutil.rmtree(tmpFolder) 
        except Exception as e:
            s3_object = s3.Object(bucket_name=bucketName, key=s3_path)
            s3_object.delete()
            all_errors.append(e) 
            print(e.message)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.')
            raise e 
            return(e)

    
    tempPath = os.path.join(tmpFolder,'images')
   
    for persons in os.listdir(tempPath):
        try:
            os.chdir(tempPath)
            if ( persons == 'drivers') :
                for driver in os.listdir(persons):                    
                    tempImagePath = os.path.join((os.path.abspath(persons)), driver)                 
                    destinationPath = 'images/drivers/' + str(driver)                 
                    s3.Bucket(bucketName).upload_file(tempImagePath, destinationPath)
                    object_acl = s3.ObjectAcl(bucketName, destinationPath)
                    response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

            if ( persons == 'owners') :
                for owner in os.listdir(persons):
                    tempImagePath = os.path.join((os.path.abspath(persons)), owner)
                    destinationPath = 'images/owners/' + str(owner)
                    s3.Bucket(bucketName).upload_file(tempImagePath, destinationPath)
                    object_acl = s3.ObjectAcl(bucketName, destinationPath)
                    response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
            
        except Exception as e:
            all_errors.append(e)
    print(all_errors)
    os.chdir("../..")
    shutil.rmtree(tmpFolder)
    s3_object = s3.Object(bucket_name=bucketName, key=s3_path)
    s3_object.delete()
    return all_errors

def taxi_csv_upload(request):
    message = 'Please Upload the Excel file here'
    if request.user.is_authenticated():
        if request.user.is_admin or request.user.is_staff:
            if request.method == "POST":
                form = TaxiDetailCsvUpload(request.POST, request.FILES)
                if form.is_valid():
                    errors = handle_taxi_xls(request.FILES['taxi_csv'],request.POST["city"])
                    print(errors)
                    if len(errors)==0:
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.\n','message2':''})
                    elif errors[0] == "xls_header_error":  
                         return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Invalid file headers to upload. Please Re-Validate and try again. \n','message2':''})     
                    elif errors[0] == "xls_file_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File not of type xls. Only xls files are accepted at the moment.\n','message2':''})
                    elif errors[0] == "network_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Network error during file upload. Please try again.\n','message2':''})                          
                    return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.','message2':'Row Number(s) '+ str((errors)) +' has invalid/duplicate data and they were NOT UPLOADED.'})
            else:
                form = TaxiDetailCsvUpload()
            return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':message})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_csv_upload")


def bulk_image_upload(request):
    message = 'Please Upload the Bulk Image ZIP here'
    secondary_message = 'The images in the zip should be named according to their traffic numbers'
    if request.user.is_authenticated():
        if request.user.is_admin or request.user.is_staff:
            if request.method == "POST":
                form = BulkImageUpload(request.POST, request.FILES)
                if form.is_valid():
                    errors = handle_bulk_image_zip(request.FILES['bulk_image_zip'])
                    if len(errors)==0:
                        return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':'Files Uploaded Successfully\n','message2':''})
                    elif errors[0] == "network_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Network error during file upload. Please try again.\n','message2':secondary_message})  

                    return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':'Files Uploaded Successfully','message2':str(len(errors))+' were NOT UPLOADED because of invalid filename.'})
            else:
                form = BulkImageUpload()
            return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':message, 'message2':secondary_message})
    else:
        return HttpResponseRedirect("/admin_login?next=bulk_image_upload")

def admin_password_change(request):
    if request.user.is_authenticated():
        return password_change(request,post_change_redirect=reverse('taxiapp:admin_password_change_done'),template_name='taxiapp/password_change.html')
    else:
        return HttpResponseRedirect("/admin_login")


def admin_password_change_done(request):
    if request.user.is_authenticated():
        return render(request, 'taxiapp/password_change_done.html')
    else:
        return HttpResponseRedirect("/admin_login")

def admin_forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = EnterPhoneNumber(request.POST)
        if form.is_valid():
            phone_number = request.POST["phone_no"]
            retrieve_user = MyUser.objects.filter(sms_number__contains=phone_number)
            if len(retrieve_user) == 0:
                return render(request, 'taxiapp/admin_forgot_password.html', {'form': form, 'message': "Could not find any exising user with the phone number. Please check and re-enter your 10-digit SMS number","message2":"FAIL"})
            else:
                 Otp_Codes.objects.filter(user=retrieve_user[0]).delete()
                 otp_code = random.randint(100000,999999)
                 code = Otp_Codes(user=retrieve_user[0],otp=str(otp_code))
                 code.save()
                 m = send_sms(str(otp_code)+" is your OTP for resetting password",phone_number,'otp') 
                 return HttpResponseRedirect("/enter_otp?number="+str(retrieve_user[0].id))
    else:
        form = EnterPhoneNumber()         
    return render(request, 'taxiapp/admin_forgot_password.html', {'form':form, 'message':"Please enter your registered 10 digit SMS number",'message2':""})

def enter_otp(request):
    if request.method == "GET":
        number = request.GET["number"]
        form = EnterOTP(initial={'user_id':int(number)})
        return render(request,'taxiapp/enter_otp.html', {'form':form, 'message':"Please enter your 6-digit OTP"})
    elif request.method == "POST":
        form = EnterOTP(request.POST)
        if form.is_valid():
            start = datetime.datetime.now() - datetime.timedelta(minutes=30)
            a = Otp_Codes.objects.filter(user_id=int(request.POST["user_id"]),otp=request.POST["otp_code"],updated_at__gte=start)
            if (len(a) == 0):
                return render(request, 'taxiapp/admin_forgot_password.html', {'form': form, 'message': "Wrong OTP","message2":"FAIL"})
            else:
                return HttpResponseRedirect('/reset_admin_password?number='+request.POST["user_id"]+"&otp="+request.POST["otp_code"])
    else:
        return HttpResponseRedirect("/")

def reset_admin_password(request):
    if request.method == "GET":
        number = request.GET["number"]
        otp_code = request.GET["otp"]
        start = datetime.datetime.now() - datetime.timedelta(minutes=30)
        a = Otp_Codes.objects.filter(user_id=int(number),otp=otp_code,updated_at__gte=start)
        if (len(a) == 0):
                return HttpResponseRedirect("/")
        else:
            form = ResetPassword(initial={'user_id':int(number)})
            return render(request, 'taxiapp/reset_admin_password.html',{'form':form,'message':"Reset Password"})
    elif request.method == "POST":
        form = ResetPassword(request.POST)
        if (form.is_valid()) and (form.cleaned_data['password'] == form.cleaned_data['confirm_password']):
            user = MyUser.objects.get(pk=int(request.POST["user_id"]))
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request,"taxiapp/reset_admin_password.html",{"form":form,"message":"Password has been successfully reset."})
        elif (form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
            form.add_error('confirm_password', 'The passwords do not match')
            return render(request, 'taxiapp/reset_admin_password.html',{'form':form,'message':"Reset Password"})
    else:
        return HttpResponseRedirect("/")

def health_check(request):
    data = {
        'result': 'success',
    }
    return JsonResponse(data) 

def handler404(request):
    response = render_to_response('taxiapp/error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('taxiapp/error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

class TaxiDriverOwner(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None, **kwargs):
        cityCode = request.GET.get('cityCode')
        rangeFrom = request.GET.get('rangeFrom')# Last five digits of Traffic Number
        rangeTo = request.GET.get('rangeTo') # Last five digits of Traffic Number
        taxiIds = request.GET.get('taxiIds') # Traffic Numbers
        numberPlates = request.GET.get('numberPlates') # Number Plates
        page = request.GET.get('page', 1) # Page Number
        limit = request.GET.get('limit', 10) # No Of Records per page
        
        vehicleDetails = Vehicle.objects.all()
        if (rangeFrom != None and rangeTo != None):
            rangeFromList = rangeFrom.split('-')
            commonStr = rangeFromList[0]+"-"+rangeFromList[1]
            rangeLen = len(rangeFromList[2])
            rangeFromValue = int(rangeFromList[2])
            rangeDiff = ( int(rangeTo.split('-')[2]) - rangeFromValue ) + 1
            rangeList = []            
            for i in range(rangeDiff):
                rangFromValuelen = len(str(rangeFromValue))
                leadingZero = rangeLen - rangFromValuelen
                rangeList.append(commonStr+"-"+str(rangeFromValue).zfill(leadingZero + rangFromValuelen))
                rangeFromValue =  rangeFromValue + 1
            print(rangeList)
            vehicleDetails = vehicleDetails.filter(traffic_number__in = rangeList)
        if (taxiIds != None):
            taxiIdsArray = taxiIds.split(',')
            vehicleDetails = vehicleDetails.filter(traffic_number__in = taxiIdsArray)
        if (numberPlates != None):
            numberPlatesArray = numberPlates.split(',')
            vehicleDetails = vehicleDetails.filter(number_plate__in = numberPlatesArray)
        if (cityCode != None):
            vehicleDetails = vehicleDetails.filter(city__city_code = cityCode)
        paginator = Paginator(vehicleDetails, limit)
        try:
            vehicleDetails = paginator.page(page)
        except PageNotAnInteger:
            vehicleDetails = paginator.page(1)
        except EmptyPage:
            vehicleDetails = paginator.page(paginator.num_pages)

        serializer = TaxiDriverOwnerSerialize(vehicleDetails,many=True)        
        return Response(data=serializer.data)

class TaxiComplaints(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None, **kwargs):
        cityCode = request.GET.get('cityCode')
        rangeFrom = request.GET.get('rangeFrom')# Last five digits of Traffic Number
        rangeTo = request.GET.get('rangeTo') # Last five digits of Traffic Number
        taxiIds = request.GET.get('taxiIds') # Traffic Numbers
        numberPlates = request.GET.get('numberPlates') # Number Plates
        page = request.GET.get('page', 1) # Page Number
        limit = request.GET.get('limit', 10) # No Of Records per page
        
        complaints = Complaint_Statement.objects.all()
        if (rangeFrom != None and rangeTo != None):
            rangeFromList = rangeFrom.split('-')
            commonStr = rangeFromList[0]+"-"+rangeFromList[1]
            rangeLen = len(rangeFromList[2])
            rangeFromValue = int(rangeFromList[2])
            rangeDiff = ( int(rangeTo.split('-')[2]) - rangeFromValue ) + 1
            rangeList = []
            for i in range(rangeDiff):
                rangFromValuelen = len(str(rangeFromValue))
                leadingZero = rangeLen - rangFromValuelen
                rangeList.append(commonStr+"-"+str(rangeFromValue).zfill(leadingZero + rangFromValuelen))
                rangeFromValue =  rangeFromValue + 1
            complaints = complaints.filter(vehicle__traffic_number__in = rangeList)
        if (taxiIds != None):
            taxiIdsArray = taxiIds.split(',')
            complaints = complaints.filter(vehicle__traffic_number__in = taxiIdsArray)
        if (numberPlates != None):
            numberPlatesArray = numberPlates.split(',')
            complaints = complaints.filter(vehicle__number_plate__in = numberPlatesArray)
        if (cityCode != None):
             complaints = complaints.filter(city__city_code = cityCode)
            

        paginator = Paginator(complaints, limit)
        try:
            complaints = paginator.page(page)
        except PageNotAnInteger:
            complaints = paginator.page(1)
        except EmptyPage:
            complaints = paginator.page(paginator.num_pages)
        
        serializer = TaxiComplaintsSerialize(complaints,many=True)        
        return Response(data=serializer.data)


def Ratings(request):
    passenger_phone = request.GET.get('passenger_phone')
    passenger_origin = request.GET.get('passenger_origin')
    passenger_destination = request.GET.get('passenger_destination')
    number_plate = request.GET.get('number_plate')
    rating_type = request.GET.get('rating_type')
    vehicleId = request.GET.get('id')
    reasons = []
    rating_type = int(rating_type)
    if(rating_type > 0):
        ratingValue = 'Unsatisfied'
        if(rating_type == 3):
            ratingValue = 'neutral'
        elif(rating_type > 3):
            ratingValue = 'Satisfied'
        ratingType = Rating_Type.objects.get(rating_type__iexact = ratingValue)
        active = Active.objects.get(active_name__iexact = 'Active')
        reasons = Rating_Reason.objects.filter(rating_type = ratingType, active = active)  

    vehicle = Vehicle.objects.get(id = vehicleId)
    drivers = Driver.objects.filter(vehicle = vehicle)

    return render(request,'taxiapp/rating.html',{'passenger_phone':passenger_phone, 'passenger_origin':passenger_origin, 
                'passenger_destination':passenger_destination, 'number_plate':number_plate, 'rating_type':rating_type, 
                'reasons':reasons,'drivers':drivers, 'vehicle_id':vehicleId})        

def customer_rating (request) :
    driver_id = request.POST.get('driver')
    reason = request.POST.get('reason')
    passenger_phone = request.POST.get('passenger_phone')
    passenger_origin = request.POST.get('passenger_origin')
    passenger_destination = request.POST.get('passenger_destination')
    rating_type = request.POST.get('rating_type')
    vehicle_id = request.POST.get('vehicle_id')
    otherReason = request.POST.get('otherReason')
    
    if(reason == 'Other'):
        reason = otherReason
    rating_type = int(rating_type)
    ratingValue = 'Unsatisfied'
    if(rating_type == 3):
        ratingValue = 'neutral'
    if(rating_type > 3):
        ratingValue = 'Satisfied'

    vehicle = Vehicle.objects.get(id = vehicle_id)
    ratingType = Rating_Type.objects.get(rating_type__iexact = ratingValue)
    customerRating = Customer_Rating ()
    driver=Driver()
    if( driver_id is not None) :
        driver = Driver.objects.get(id = driver_id)
        customerRating.driver = driver
    
    
    customerRating.vehicle = vehicle
    customerRating.rating_type = ratingType
    
    customerRating.reason = reason
    customerRating.phone_number = passenger_phone
    customerRating.destination_area = passenger_destination
    customerRating.origin_area = passenger_origin
    # Who's name we have to keep as created by and modified by
    #customerRating.created_by = passenger_phone
    #customerRating.modified_by = passenger_phone

    customerRating.save()
    return render(request,'taxiapp/rating.html',{'msg':'Thank you for your rating.'})

def OwnerImagesMigration(request):
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    #owners = Owner.objects.all()
    path = 'drivers/'
    owners = Owner.objects.filter(owner_image__startswith = path)
    ownerDestPath = "images/owners/"
    for owner in owners :
        if(owner.owner_image == 'drivers/profile.png'):
            owner.owner_image = 'images/profile.png'
            owner.save()
        elif(owner.owner_image is not None and owner.owner_image != 'drivers/profile.png'):
            ownerImage = str(owner.owner_image)
            if('/' in ownerImage):
                ownerImage = ownerImage.split('/')[1]                
            try:
                dest = s3.Bucket(bucketName)
                source= { 'Bucket' : bucketName, 'Key': str(owner.owner_image)}
                dest.copy(source, ownerDestPath + ownerImage)
                #Grant public Permisions
                object_acl = s3.ObjectAcl(bucketName, ownerDestPath + ownerImage)
                response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
                
                owner.owner_image = ownerDestPath + ownerImage
                owner.save()
            except Exception as e:
                print(e)
    return render(request,'taxiapp/migration.html') 

def DriverImagesMigration(request):
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    path = 'drivers/'
    drivers = Driver.objects.filter(driver_image__startswith=path)
    driverDestPath = "images/drivers/"
    for driver in drivers :
        if(driver.driver_image == 'drivers/profile.png'):
            driver.driver_image = 'images/profile.png'
            driver.save()
        elif(driver.driver_image is not None and driver.driver_image != 'drivers/profile.png'):
            driverImage = str(driver.driver_image)
            if('/' in driverImage):
                driverImage = driverImage.split('/')[1]                
            try:
                dest = s3.Bucket(bucketName)
                source= { 'Bucket' : bucketName, 'Key': str(driver.driver_image)}
                dest.copy(source, driverDestPath + driverImage)
                #Grant public Permisions
                object_acl = s3.ObjectAcl(bucketName, driverDestPath + driverImage)
                response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

                driver.driver_image = driverDestPath + driverImage
                driver.save()
            except Exception as e:
                print(e)
    return render(request,'taxiapp/migration.html')

# def VehicleQrCodeMigration(request):
#     bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
#     s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#     vehicles = Vehicle.objects.all()
#     destPath = "qr_codes/vehicles/"
#     for vehicle in vehicles :
#         qr_code = str(vehicle.qr_code)
#         if('/' in qr_code):
#             qr_code = qr_code.split('/')[1]                
#         try:
#             dest = s3.Bucket(bucketName)
#             source= { 'Bucket' : bucketName, 'Key': str(vehicle.qr_code)}
#             #source= { 'Bucket' : "taxipublic", 'Key': str(vehicle.qr_code)}
#             #print(source)
#             dest.copy(source, destPath + qr_code)
#             vehicle.qr_code = destPath + qr_code
#             vehicle.save()
#         except Exception as e:
#             print(e)
#     return render(request,'taxiapp/migration.html')

# def DriverQrCodeMigration(request):
#     bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
#     s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#     drivers = Driver.objects.all()
#     destPath = "qr_codes/drivers/"
#     for driver in drivers :
#         qr_code = str(driver.qr_code)
#         if('/' in qr_code):
#             qr_code = qr_code.split('/')[1]                
#         try:
#             dest = s3.Bucket(bucketName)
#             source= { 'Bucket' : bucketName, 'Key': str(driver.qr_code)}
#             #source= { 'Bucket' : "taxipublic", 'Key': str(driver.qr_code)}
#             dest.copy(source, destPath + qr_code)
#             driver.qr_code = destPath + qr_code
#             driver.save()
#         except Exception as e:
#             print(e)
#     return render(request,'taxiapp/migration.html')


# def ImageGrandPublic(request):
#     mainFolder = request.GET.get('mainFolder')
#     subFolder = request.GET.get('subFolder')
#     folder = str(mainFolder) +'/'+ str(subFolder)
#     print(folder)
#     bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
#     s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#     bucket = s3.Bucket(bucketName)
#     for key in bucket.objects.filter(Prefix=folder):
#         fileName = key.key
#         print(fileName)
#         object_acl = s3.ObjectAcl(bucketName, fileName)
#         response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
#     print('Done')
#     return render(request,'taxiapp/migration.html')

def DriverImageValidation(request):
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    drivers = Driver.objects.filter(is_image_verified=False)
    destPath = "images/drivers/"
    for driver in drivers :
        if(driver.driver_image_name is not None and driver.driver_image_name != '' 
            and driver.driver_image_name != '-' and driver.driver_image_name != 'profile.png'):
            if(driver.driver_image is None or driver.driver_image == '' 
                or driver.driver_image == '-' or driver.driver_image == 'images/profile.png'):  
                bucket = s3.Bucket(bucketName)                                   
                fileName = 'drivers/'+driver.driver_image_name
                objs = list(bucket.objects.filter(Prefix=fileName))
                if len(objs) > 0:
                    source= { 'Bucket' : bucketName, 'Key': fileName}
                    destination = destPath + driver.driver_image_name
                    bucket.copy(source, destination)

                    object_acl = s3.ObjectAcl(bucketName, destination)
                    response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

                    driver.driver_image = destination
                    driver.is_image_verified = True
                    driver.save()
            else:
                bucket = s3.Bucket(bucketName)                                   
                fileName = str(driver.driver_image)
                objs = list(bucket.objects.filter(Prefix=fileName))
                if (len(objs) == 0):
                    fileName = 'drivers/'+driver.driver_image_name
                    objs1 = list(bucket.objects.filter(Prefix=fileName))
                    if len(objs1) > 0:
                        source= { 'Bucket' : bucketName, 'Key': fileName}
                        destination = destPath + driver.driver_image_name
                        bucket.copy(source, destination)

                        object_acl = s3.ObjectAcl(bucketName, destination)
                        response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

                        driver.driver_image = destination
                        driver.is_image_verified = True
                        driver.save()
                else:
                    driver.is_image_verified = True
                    driver.save()
        elif(driver.driver_image_name is None or driver.driver_image_name == '' 
            or driver.driver_image_name == '-' or driver.driver_image_name == 'profile.png'):

            if(driver.driver_image_name != 'profile.png'):
                driver.driver_image_name = 'profile.png'
            if(driver.driver_image != 'images/profile.png'):
                driver.driver_image = 'images/profile.png'

            driver.is_image_verified = True
            driver.save()


    return render(request,'taxiapp/migration.html')


def OwnerImageValidation(request):
    bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    owners = Owner.objects.filter(is_image_verified=False)
    destPath = "images/owners/"
    for owner in owners :
        if(owner.owner_image_name is not None and owner.owner_image_name != '' 
            and owner.owner_image_name != '-' and owner.owner_image_name != 'profile.png'):
            if(owner.owner_image is None or owner.owner_image == '' 
                or owner.owner_image == '-' or owner.owner_image == 'images/profile.png'):  
                bucket = s3.Bucket(bucketName)                                   
                fileName = 'drivers/'+owner.owner_image_name
                objs = list(bucket.objects.filter(Prefix=fileName))
                if len(objs) > 0:
                    source= { 'Bucket' : bucketName, 'Key': fileName}
                    destination = destPath + owner.owner_image_name
                    bucket.copy(source, destination)
                    
                    object_acl = s3.ObjectAcl(bucketName, destination)
                    response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

                    owner.owner_image = destination
                    owner.save()
            
            else:
                bucket = s3.Bucket(bucketName)                                   
                fileName = str(owner.owner_image)
                objs = list(bucket.objects.filter(Prefix=fileName))
                if (len(objs) == 0):
                    fileName = 'drivers/'+owner.owner_image_name
                    objs1 = list(bucket.objects.filter(Prefix=fileName))
                    if len(objs1) > 0:
                        source= { 'Bucket' : bucketName, 'Key': fileName}
                        destination = destPath + owner.owner_image_name
                        bucket.copy(source, destination)

                        object_acl = s3.ObjectAcl(bucketName, destination)
                        response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)

                        owner.owner_image = destination
                        owner.is_image_verified = True
                        owner.save()
                else:
                    owner.is_image_verified = True
                    owner.save()

        elif(owner.owner_image_name is None or owner.owner_image_name == '' 
            or owner.owner_image_name == '-' or owner.owner_image_name == 'profile.png'):

            if(owner.owner_image_name != 'profile.png'):
                owner.owner_image_name = 'profile.png'
            if(owner.owner_image != 'images/profile.png'):
                owner.owner_image = 'images/profile.png'

            owner.is_image_verified = True
            owner.save()
            
            
    return render(request,'taxiapp/migration.html')

def Terms_Of_Use(request):
    return render(request,'terms_of_use.html')

def Privacy_Policy(request):
    return render(request,'privacy_policy.html')
def About_Us(request):
    return render(request,'about_us.html')

def Vehice_Registration(request):
    
    cities = City_Code.objects.all()
    print(cities)
    return render(request,'taxiapp/vehicle_registration.html',{'cities':cities})

def Vehicle_Register_Details(request):
    traffic_number=request.POST.get('traffic_number')
    number_plate=request.POST.get('number_plate')
    autostand=request.POST.get('autostand')
    insurance=request.POST.get('insurance')
    union=request.POST.get('union')
    pollution=request.POST.get('pollution')
    engine_number=request.POST.get('engine_number')
    chasis_number=request.POST.get('chasis_number')
    rc_expiry=request.POST.get('rc_expiry')
    rc_number=request.POST.get('rc_number')
    num_of_complaints=0
    
    active = Active.objects.get(active_name__iexact = 'Inactive')
    #Set city code object by getting from table
    city_code =request.POST.get('city_code')
    city = City_Code.objects.get(city_code=city_code)
    vehicle_type = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    # created_by=''
    # modified_by=''
    capacity_of_passengers=request.POST.get('capacity_of_passengers')
    Owner_name =request.POST.get('Owner_name')
   
    Owner_Phone_no =request.POST.get('Owner_Phone_no')

    v1=Vehicle_Registration(traffic_number=traffic_number,number_plate=number_plate,autostand=autostand,
    insurance=insurance,union=union,pollution=pollution,engine_number=engine_number,chasis_number=chasis_number,
    rc_expiry=rc_expiry,rc_number=rc_number,num_of_complaints=num_of_complaints,created_by=Owner_name,
    modified_by=Owner_name,active=active,city=city,vehicle_type=vehicle_type,
    capacity_of_passengers=capacity_of_passengers)
    v1.save() 
    #Send SMS which you captured owner name and PH No
    message = 'Hi Mr ' + ' Owner Name: ' + str(Owner_name) + ' successfully vehicle registration.'
    m = send_sms(message,Owner_Phone_no,'complaint')
    #form = TaxisearchForm()
#   return render(request,'vehicle_register_success.html',{'message':'successfully registered.'})
    #return render(request, 'taxiapp/drivers_list.html', {'message':'successfully registered.','form' : form})
    return HttpResponseRedirect("/?message=successfully registered.")

def Add_Vehicle(request):
    cities = City_Code.objects.values_list('city', flat=True).distinct()
    vehice_type=Vehicle_type.objects.values_list('vehicle_type', flat=True).distinct()
    return render(request,'taxiapp/add_vehicle.html',{'cities':cities,'vehice_type':vehice_type})

def Add_Driver(request):
    vehicle_type=Vehicle_type.objects.values_list('vehicle_type', flat=True).distinct()
    return render(request,'taxiapp/add_driver.html',{'vehicle_type':vehicle_type})

def Add_Vehicle_Details(request):

    print("********************")
    print(request.POST)
    


    #Read Owner Details
    owner_name = request.POST.get('o_owner_name')
    address = request.POST.get('o_address')
    date_of_birth =request.POST.get('o_date_of_birth')
    son_of =request.POST.get('o_son_of')
    phone_number =request.POST.get('o_phone_number')
    aadhar_number =request.POST.get('o_aadhar_number')
    dl_number =request.POST.get('o_dl_number')
    dl_expiry =request.POST.get('o_dl_expiry')
    
    owner = Owner(
      owner_name = owner_name,
      address = address,
      date_of_birth = date_of_birth,
      son_of =son_of,
      phone_number = phone_number,
      aadhar_number = aadhar_number,
      dl_number = dl_number,
      dl_expiry = dl_expiry,
      #active = models.ForeignKey(Active,null=True)
	  )

    owner.save()
      
    #Read Vehicle Details
    traffic_number=request.POST.get('v_traffic_number')
    number_plate=request.POST.get('v_number_plate')
    autostand=request.POST.get('v_autostand')
    insurance=request.POST.get('v_insurance')
    union=request.POST.get('v_union')
    pollution=request.POST.get('v_pollution')
    engine_number=request.POST.get('v_engine_number')
    chasis_number=request.POST.get('v_chasis_number')
    rc_expiry=request.POST.get('v_rc_expiry')
    # rc_number=request.POST.get('rc_number')
    num_of_complaints=0
    active = Active.objects.get(active_name__iexact = 'Inactive')
    #Set city code object by getting from table
    city =request.POST.get('v_city')
    city = City_Code.objects.get(city=city)
    vehicle_type = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    capacity_of_passengers=request.POST.get('v_capacity_of_passengers')
    vehicle=Vehicle(traffic_number=traffic_number,number_plate=number_plate,autostand=autostand,
    insurance=insurance,union=union,pollution=pollution,engine_number=engine_number,
    chasis_number=chasis_number,rc_expiry=rc_expiry,num_of_complaints=num_of_complaints,
    active=active,city=city,vehicle_type=vehicle_type,capacity_of_passengers=capacity_of_passengers,owner = owner)
    vehicle.save()
    
    #Read Driver Details
    #traffic_number=request.POST.get('traffic_number')
    driver_name_list=request.POST.getlist('d_driver_name')
    address_list=request.POST.getlist('d_address')
    date_of_birth_list=request.POST.getlist('d_date_of_birth')
    son_of_list=request.POST.getlist('d_son_of')
    phone_number_list=request.POST.getlist('d_phone_number')
    aadhar_number_list=request.POST.getlist('d_aadhar_number')
    dl_number_list=request.POST.getlist('d_dl_number')
    dl_expiry_list=request.POST.getlist('d_dl_expiry')
    # vehicle=request.POST.get('vehicles')
    # # vehicle = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    if len(driver_name_list) > 0 :
        for (driver_name,address,date_of_birth,son_of,phone_number,aadhar_number,dl_number,dl_expiry) in zip(
        driver_name_list,address_list,date_of_birth_list,son_of_list,phone_number_list,
        aadhar_number_list,dl_number_list,dl_expiry_list) :
            driver = Driver(
                        # traffic_number=traffic_number,
                        driver_name=driver_name,
                        address=address,
                        date_of_birth=date_of_birth,
                        son_of=son_of,
                        phone_number=phone_number,
                        aadhar_number=aadhar_number,
                        dl_number=dl_number,
                        dl_expiry=dl_expiry,
                        vehicle=vehicle)
            driver.save()
        return render(request, 'taxiapp/taxi_list.html', {'msg_vehicle_list':'successfully \
        Vehicle added.'})
        
    return render(request, 'taxiapp/taxi_list.html', {'msg_vehicle_list':'Unabled to add \
    Vehicle/Owner/Drivers Details. Please validate input fields and retry'})

def Add_Driver_Details(request):
    traffic_number=request.POST.get('traffic_number')
    driver_name=request.POST.get('driver_name')
    address=request.POST.get('address')
    date_of_birth=request.POST.get('date_of_birth')
    son_of=request.POST.get('son_of')
    phone_number=request.POST.get('phone_number')
    aadhar_number=request.POST.get('aadhar_number')
    dl_number=request.POST.get('dl_number')
    dl_expiry=request.POST.get('dl_expiry')
    vehicle=request.POST.get('vehicles')
    # driver_image=request.Files['driver_image']
    # vehicle=Vehicle_type.objects.get(vehicle_type=vehicle)
    # vehicle = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    dr=Driver(traffic_number=traffic_number,driver_name=driver_name,address=address,date_of_birth=date_of_birth,
    son_of=son_of,phone_number=phone_number,aadhar_number=aadhar_number,dl_number=dl_number,dl_expiry=dl_expiry,
    vehicle=vehicle)
    dr.save()
    return render(request, 'taxiapp/taxi_list.html', {'msg_vehicle_list':'successfully Driver details added.'})

def Add_Owner_Details(request):
    traffic_number=request.POST.get('traffic_number')
    driver_name=request.POST.get('driver_name')
    address=request.POST.get('address')
    date_of_birth=request.POST.get('date_of_birth')
    son_of=request.POST.get('son_of')
    phone_number=request.POST.get('phone_number')
    aadhar_number=request.POST.get('aadhar_number')
    dl_number=request.POST.get('dl_number')
    dl_expiry=request.POST.get('dl_expiry')
    vehicle=request.POST.get('vehicles')
    # driver_image=request.Files['driver_image']
    # vehicle=Vehicle_type.objects.get(vehicle_type=vehicle)
    # vehicle = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    dr=Driver(traffic_number=traffic_number,driver_name=driver_name,address=address,date_of_birth=date_of_birth,
    son_of=son_of,phone_number=phone_number,aadhar_number=aadhar_number,dl_number=dl_number,dl_expiry=dl_expiry,
    vehicle=vehicle)
    dr.save()
    return render(request, 'taxiapp/taxi_list.html', {'msg_vehicle_list':'successfully Driver details added.'})



     
