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
import StringIO
from . import constants
import urllib,shutil,os,zipfile
from datetime import date, tzinfo, datetime, timedelta
from django.db.models import Q
import csv
from django.utils.encoding import smart_str 



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
    # """ Code : Using Cutly Acccess Token """
    # req = urllib2.Request(constants.CUTLY_API+'?key='+constants.CUTLY_ACCESS_TOKEN+'&short='+url)
    # f = urllib2.urlopen(req)
    # resJson = (simplejson.loads(f.read())['url'])
    # return resJson['shortLink']
    # """ Code : Using Cutly Acccess Token """
    
# """ Code : Using Cutly Acccess Token """
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(constants.CUTLY_API+'?key='+constants.CUTLY_ACCESS_TOKEN+'&short='+url,headers=hdr)
    f = urllib2.urlopen(req)
    resJson = (simplejson.loads(f.read())['url'])
    return resJson['shortLink']
# """ Code : Using Cutly Acccess Token """

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
    nex = request.GET.get('next', 'dashboard')
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
        number_plate = request.GET.get('number_plate', '')
        passenger_phone = request.GET.get('passenger_phone','')
        passenger_origin = request.GET.get('passenger_origin','')
        passenger_destination = request.GET.get('passenger_destination','')
        form = ComplaintUserForm(initial={'vehicle':vehicle_id, 'number_plate':number_plate,'phone_number':passenger_phone,\
               'origin_area':passenger_origin,'destination_area':passenger_destination})
        form.fields['vehicle'].widget = forms.TextInput(attrs={'size':'30','readonly':"True"})
        form.fields['number_plate'].widget = forms.TextInput(attrs={'size':'30','readonly':"True"})
        return render(request, 'taxiapp/complaint.html', {'form': form})


def send_sms(message,phone_number,kind):
    if kind == 'complaint':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161522289414352}) 
    elif kind == 'ack':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161522368108689})
    elif kind == 'sos':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161522364569729})
    elif kind == 'otp':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161347685466404})
    elif kind == 'register':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161347690371861})
    elif kind == 'resolved':
        r = requests.get(constants.SMS_API_URL, params={'username':constants.SMS_USERNAME,'password':constants.SMS_PASSWORD,'from':constants.SMS_HEADER,'to':str(phone_number),'msg':str(message),'type':constants.SMS_TYPE, 'template_id':1707161347681335353})
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
        complaint.created_time = datetime.now()
        complaint.save()
        #taxi = Taxi_Detail.objects.get(id=complaint.taxi.id)
        vehicleObj = Vehicle.objects.get(id=complaint.vehicle.id)
        driver = Driver()
        try:        
            driver = Driver.objects.get(vehicle = vehicleObj)
        except Exception as e:
            print(e.message)
        map_url = 'https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''
        number_plate = vehicleObj.number_plate if vehicleObj and vehicleObj.number_plate else ''
        driver_name = driver.driver_name if driver and driver.driver_name else ''
        driver_phone_number = driver.phone_number if driver and driver.phone_number else ''
        complaint_complaint = complaint.complaint if complaint and complaint.complaint else ''
        complaint_phone_number = complaint.phone_number if complaint and complaint.phone_number else ''
        destination_area = complaint.destination_area if complaint and  complaint.destination_area else ''
        message = 'Complaint Name: ' + str(driver_name) + '\nTaxi Number: ' + str(number_plate) \
                  + '\nDriver Phone Number: ' + str(driver_phone_number) + '\nComplaint Reason: ' \
                  + str(complaint_complaint) + '\nLocation: ' + googl(map_url) + '\nPassenger Phone Number: ' \
                  + str(complaint_phone_number) + '\nOrigin: ' + str(googl(complaint.origin_area)) + '\nDestination: ' \
                  + str(destination_area) + '\nVALVDATA'
        message1 = 'Your Complaint has been registered.\nTaxi Number: ' + str(number_plate) + '\nDriver Name: ' \
                   + str(driver_name) + '\nDriver Phone Number: ' + str(driver_phone_number + '\nVALVDATA')
        if vehicleObj.city.sms:
            m = send_sms(message,phone_number,'complaint')
            n = send_sms(message1, complaint_phone_number, 'ack')
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
        complaintStatement.resolved_time = datetime.now()
        complaintStatement.save()
        
        resolved_date = complaintStatement.resolved_time
        resolved_date.strftime('%m-%d-%y %H:%M:%S')
        reason = ""
        if(complaintStatement.reason != None):
            reason = str(complaintStatement.reason.reason)
        
        print(resolved_date)
        smsMessage = 'Complaint Resolved.\n'+'Taxi Number: '+str(complaintStatement.vehicle.number_plate)+'\nDate: '+str(resolved_date)+'\nComplaint Reason: '+reason+'\nResolution: '+str(message +'\n'+ 'VALVDATA')
        
        print(smsMessage)
        print(complaintStatement.phone_number)
        m = send_sms(smsMessage,str(complaintStatement.phone_number),'resolved')
        return HttpResponseRedirect("/complaints_list") 
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
        activeTab = request.GET.get('activeTab','dashboard')
    else:
        page = request.POST.get('page', 1)
        activeTab = request.POST.get('activeTab')
    
    message = request.GET.get('message','')    
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
            #vehicleregistrations = Vehicle_Registration.objects.all()
            #active = Active.objects.get(active_name__iexact = "active") 
            #vehicleregistrations = Vehicle_Registration.objects.filter(active = active)
            dashboardDict = getDashboardData(None)
        else :
            #city = City_Code.objects.get(city_code = city_code)
            rows = Vehicle.objects.select_related().filter(city = city)
            rows_c = Complaint_Statement.objects.filter(city=city)
            ratings = Customer_Rating.objects.filter(vehicle__city = city)
            #active = Active.objects.get(active_name__iexact = "active") 
            #vehicleregistrations = Vehicle_Registration.objects.select_related().filter(city = city).filter(active = active)
            #vehicleregistrations = Vehicle_Registration.objects.select_related().filter(city = city)
            dashboardDict = getDashboardData(city)


        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            rows = rows.filter(vehicle_type=vehicle_type)
            rows_c = rows_c.filter(vehicle__vehicle_type=vehicle_type)
            ratings = ratings.filter(vehicle__vehicle_type=vehicle_type)
            #vehicleregistrations=vehicleregistrations.filter(vehicle_type=vehicle_type)
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
            #vehicleregistrations=vehicleregistrations.filter(traffic_number__in = rangeList)
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
            #vehicleregistrations=vehicleregistrations.filter(traffic_number__in = taxiIdsArray)
            
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
            print(numberPlates)
            numberPlatesArray = numberPlates.split(',')
            print(numberPlatesArray)
            print(len(rows))
            rows = rows.filter(number_plate__in = numberPlatesArray)
            print(len(rows))
            rows_c=rows_c.filter(vehicle__number_plate__in = numberPlatesArray)
            ratings=ratings.filter(vehicle__number_plate__in = numberPlatesArray)
            #vehicleregistrations=vehicleregistrations.filter(number_plate__in = numberPlatesArray)
           
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

        active = Active.objects.get(active_name__iexact = 'Active')
        vehicleregistrations=Vehicle_Registration.objects.filter(active=active, registered = False)
        
        drivers=Driver.objects.all()
        # print("**********************")
        # print(request.POST)
        # driver_type = request.POST.get('driverType')
        # print(driver_type)
        # if (driver_type == None or driver_type == 'Unallocated' ) :
        #     driver_type = 'Unallocated'
        #     drivers = drivers.filter(vehicle = None)
        # else :
        #     driverType = 'Allocated'
        #     drivers = drivers.filter(~Q(vehicle = None))
        
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
        #'vehicleregistrations':vehicleregistrations,'rangeTo':rangeTo,'taxiIds':taxiIds,
        'rangeTo':rangeTo,'taxiIds':taxiIds,
        'vehicleregistrations': vehicleregistrations,
        #'driverType':driver_type,
        'user':request.user,'message':message,'activeTab':activeTab,'drivers':drivers})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_list")

def getDashboardData(city):
    dashboardDict = {}
    if(city is not None):
        # To get today registration count
        #timestamp_from = datetime.now().date() - timedelta(days=1)
        currentDate = datetime.now().date()
        #print(timestamp_from,timestamp_to)
        todayVR = Vehicle.objects.filter(city = city, created_time__date = currentDate ).distinct() 
        dashboardDict.update(todayVR = todayVR)
        # To get last 1 week registration count
        timestamp_from = currentDate - timedelta(days=7)
        #timestamp_to = datetime.now().date()
        thisWeekVR = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisWeekVR = thisWeekVR)
        # To get last 1 month registration count
        timestamp_from = currentDate - timedelta(days=30)
        #timestamp_to = datetime.now().date()
        thisMonthVR = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisMonthVR = thisMonthVR)
        # To get last 1 year registration count
        timestamp_from = currentDate - timedelta(days=365)
        #timestamp_to = datetime.now().date()
        thisYearVR = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisYearVR = thisYearVR)
        # To get total count of records
        # total = len ( Vehicle.objects.all())
        # dashboardDict.update(total = total)
        total = Vehicle.objects.filter(city = city)
        dashboardDict.update(total = total)
    else:
        # To get today registration count
         #timestamp_from = datetime.now().date() - timedelta(days=1)
        currentDate = datetime.now().date()
        #print(timestamp_from,timestamp_to)
        todayVR = Vehicle.objects.filter(created_time__date = currentDate ).distinct() 
        dashboardDict.update(todayVR = todayVR)
        # To get last 1 week registration count
        timestamp_from = currentDate - timedelta(days=7)
        #timestamp_to = datetime.now().date()
        thisWeekVR = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisWeekVR = thisWeekVR)
        # To get last 1 month registration count
        timestamp_from = currentDate - timedelta(days=30)
        #timestamp_to = datetime.now().date()
        thisMonthVR = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisMonthVR = thisMonthVR)
        # To get last 1 year registration count
        timestamp_from = currentDate - timedelta(days=365)
        #timestamp_to = datetime.now().date()
        thisYearVR = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(thisYearVR = thisYearVR)
        # To get total count of records
        total =  Vehicle.objects.all()
        dashboardDict.update(total = total)
    return dashboardDict


def getDashboardDataWeekly(city):
    dashboardDict = {}
    if(city is not None):
        # To get today registration count
        #timestamp_from = datetime.now().date() - timedelta(days=1)
        currentDate = datetime.now().date()
        day0 = Vehicle.objects.filter(city = city, created_time__date = currentDate ).distinct() 
        dashboardDict.update(day0 = day0)
       
        timestamp_from = currentDate - timedelta(days=1)
        day1 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day1 = day1)
       
        timestamp_from = currentDate - timedelta(days=2)
        day2 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day2 = day2)
       
        timestamp_from = currentDate - timedelta(days=3)
        day3 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day3 = day3)

        timestamp_from = currentDate - timedelta(days=4)
        day4 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day4 = day4)

        timestamp_from = currentDate - timedelta(days=5)
        day5 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day5 = day5)

        timestamp_from = currentDate - timedelta(days=6)
        day6 = Vehicle.objects.filter(city = city, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day6 = day6)
        # To get total count of records
        # total = len ( Vehicle.objects.all())
        # dashboardDict.update(total = total)
        total = Vehicle.objects.filter(city = city)
        dashboardDict.update(total = total)
    else:
        currentDate = datetime.now().date()
        day0 = Vehicle.objects.filter(created_time__date = currentDate ).distinct() 
        dashboardDict.update(day0 = day0)
       
        timestamp_from = currentDate - timedelta(days=1)
        day1 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day1 = day1)
       
        timestamp_from = currentDate - timedelta(days=2)
        day2 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day2 = day2)
       
        timestamp_from = currentDate - timedelta(days=3)
        day3 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day3 = day3)

        timestamp_from = currentDate - timedelta(days=4)
        day4 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day4 = day4)

        timestamp_from = currentDate - timedelta(days=5)
        day5 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day5 = day5)

        timestamp_from = currentDate - timedelta(days=5)
        day6 = Vehicle.objects.filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDict.update(day6 = day6)

        total =  Vehicle.objects.all()
        dashboardDict.update(total = total)
    return dashboardDict

def getDashboardDataVehicleType(dashboardDict,vehicleType):
   
    dashboardDictvehicle = {}

    if(vehicleType is not None):
        
        currentDate = datetime.now().date()
        todayVR = dashboardDict['todayVR'].filter(vehicle_type = vehicleType, created_time__date = currentDate ).distinct()
        dashboardDictvehicle.update(todayVR = todayVR)
        
        timestamp_from = currentDate - timedelta(days=7)
        
        thisWeekVR = dashboardDict['thisWeekVR'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(thisWeekVR = thisWeekVR)
        
        timestamp_from = currentDate - timedelta(days=30)
        
        thisMonthVR = dashboardDict['thisMonthVR'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(thisMonthVR = thisMonthVR)
        
        timestamp_from = currentDate - timedelta(days=365)
        
        thisYearVR = dashboardDict['thisYearVR'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(thisYearVR = thisYearVR)

        total = dashboardDict['total'].filter(vehicle_type = vehicleType).distinct() 
        dashboardDictvehicle.update(total = total)
        
    else:
        
        currentDate = datetime.now().date()
        
        todayVR = dashboardDict['todayVR'].filter(created_time__date = currentDate ).distinct() 
        dashboardDictvehicle.update(todayVR = todayVR)
        
        timestamp_from = currentDate - timedelta(days=7)
        
        thisWeekVR = dashboardDict['thisWeekVR'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(thisWeekVR = thisWeekVR)
        
        timestamp_from = currentDate - timedelta(days=30)
        
        thisMonthVR = dashboardDict['thisMonthVR'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(thisMonthVR = thisMonthVR)
        
        timestamp_from = currentDate - timedelta(days=365)
        
        thisYearVR = dashboardDict['thisYearVR'].filter(created_time__date__gte = timestamp_from,created_time__date__lte = currentDate).distinct() 
        dashboardDictvehicle.update(thisYearVR = thisYearVR)

        total = dashboardDict['total']
        dashboardDictvehicle.update(total = total)
        
        
    return dashboardDictvehicle

def getWeeklyDashboardDataVehicleType(dashboardDict,vehicleType):
   
    dashboardDictvehicle = {}

    if(vehicleType is not None):
        
        currentDate = datetime.now().date()
        day0 = dashboardDict['day0'].filter(vehicle_type = vehicleType, created_time__date = currentDate ).distinct()
        dashboardDictvehicle.update(day0 = day0)
        
        timestamp_from = currentDate - timedelta(days=1)
        day1 = dashboardDict['day1'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day1 = day1)
        
        timestamp_from = currentDate - timedelta(days=2)
        day2 = dashboardDict['day2'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day2 = day2)

        timestamp_from = currentDate - timedelta(days=3)
        day3 = dashboardDict['day3'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day3 = day3)

        timestamp_from = currentDate - timedelta(days=4)
        day4 = dashboardDict['day4'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day4 = day4)

        timestamp_from = currentDate - timedelta(days=5)
        day5 = dashboardDict['day5'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day5 = day5)

        timestamp_from = currentDate - timedelta(days=6)
        day6 = dashboardDict['day6'].filter(vehicle_type = vehicleType, created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day6 = day6)

        total = dashboardDict['total'].filter(vehicle_type = vehicleType).distinct() 
        dashboardDictvehicle.update(total = total)
        
    else:
        
        currentDate = datetime.now().date()
        day0 = dashboardDict['day0'].filter(created_time__date = currentDate ).distinct()
        dashboardDictvehicle.update(day0 = day0)
        
        timestamp_from = currentDate - timedelta(days=1)
        day1 = dashboardDict['day1'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day1 = day1)
        
        timestamp_from = currentDate - timedelta(days=2)
        day2 = dashboardDict['day2'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day2 = day2)

        timestamp_from = currentDate - timedelta(days=3)
        day3 = dashboardDict['day3'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day3 = day3)

        timestamp_from = currentDate - timedelta(days=4)
        day4 = dashboardDict['day4'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day4 = day4)

        timestamp_from = currentDate - timedelta(days=5)
        day5 = dashboardDict['day5'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day5 = day5)

        timestamp_from = currentDate - timedelta(days=6)
        day6 = dashboardDict['day6'].filter(created_time__date__gte = timestamp_from,created_time__date__lt = currentDate).distinct() 
        dashboardDictvehicle.update(day6 = day6)

        total = dashboardDict['total']
        dashboardDictvehicle.update(total = total)
        
        
    return dashboardDictvehicle



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
        print(point)
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
            cs.latitute = str(lat)
            cs.longitude = str(lon) 
            cs.city = city
            cs.area = area
            cs.origin_area = p_origin
            cs.destination_area = p_destination
            cs.phone_number = p_phone
            cs.assigned_to = police
            cs.resolved = False
            cs.is_emergency_text = True 
            cs.complaint_number = city.city_code+'-CN-'+str(city.complaint_no+1).zfill(7)
            cs.reason = Reasons.objects.get(reason__iexact = 'Emergency text')
            cs.created_by = p_phone
            cs.created_time = datetime.now()
            cs.save()

            cs_id = cs.id

            city.complaint_no = city.complaint_no+1
            city.save()

            
            # message = 'Emergency SOS\nName: '+str(driver.driver_name)+'\nTaxi Number: '+str(vehicle.number_plate)+'\nDriver Phone Number:'+str(driver.phone_number)+'\nLocation: '+str(googl('https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''))+'\nPassenger Phone Number:'+str(p_phone)+'\nOrigin:'+str(p_origin)+'\nDestination:'+str(p_destination) +'\nVALVDATA'
            message = 'Emergency SOS\nName: ' + str(driver.driver_name) + '\nTaxi Number: ' + str(vehicle.number_plate)\
                      + '\nDriver Phone Number:' + str(driver.phone_number) + '\nLocation: ' \
                      + str(googl('https://www.mytaxisafe.com/get_taxi_location/' + str(cs_id) + '')) \
                      + '\nPassenger Phone Number:' + str(p_phone) + '\nOrigin:' + str(googl(p_origin)) \
                      + '\nDestination:' + str(p_destination) + '\nVALVDATA'
            message1 = 'Your SOS has been registered.\nTaxi Number: '+str(vehicle.number_plate)+'\nDriver Name: '+str(driver.driver_name)+'\nDriver Phone Number: '+str(driver.phone_number)+'\nVALVDATA'
            # message1 = 'Your SOS has been registered.\nTaxi Number: '+str(vehicle.number_plate)+'\nDriver Name: '+str(driver.driver_name)+'\nDriver Phone Number: '+str(driver.phone_number)+'\nLocation: http://localhost:8001/get_taxi_location/'+str(cs_id)+'/ \nVALVDATA'
            if vehicle.city.sms:
                m = send_sms(message,phone_number,'sos')
                n = send_sms(message1,p_phone,'ack')
                # Added new column messaging_number in City_Code and send message. 
                if(city.messaging_number is not None and city.messaging_number != ''):
                    l = send_sms(message,city.messaging_number,'sos')
            if vehicle.city.whatsapp:
                m = send_whatsapp(message,whatsapp_number)
            return render(request,'taxiapp/taxi_emergency.html',{'message':'', 'distance':min_distance,'police':police, 'cs_id':str(cs_id)})
        else:
            return render(request,'taxiapp/taxi_emergency.html',{'message':'There is no police station nearby.'})
    else:
            return render(request,'taxiapp/error.html')

def taxi_emergency_location(request, pk):
    location = Complaint_Statement.objects.get(id=pk)
    csrf_token = request.COOKIES.get('csrftoken')
    return render(request, 'taxiapp/taxi_emergency_location.html', {'location': location, 'csrf_token':csrf_token})
    # return render(request,'taxiapp/taxi_emergency_location.html')
    # if request:
    #     latitude = request.POST.get('latitude')
    #     longitude = request.POST.get('longitude')
        
    #     location_url= 'https://www.google.co.in/maps/place/'+latitude+','+longitude+''
    #     # Save the location data to your database or perform any other necessary actions
    #     # ...

    #     return render(request,'taxiapp/taxi_emergency_location.html', {'location_url':location_url, 'pk':pk})
    # else:
    #     return HttpResponse(status=400)get_taxi_location


def update_location(request):
    user_id = request.POST.get('id')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    location = Complaint_Statement.objects.get(id=user_id)
    location.latitute = latitude
    location.longitude = longitude
    # location = Complaint_Statement(id=user_id, latitute=latitude, longitude=longitude)
    location.save()
    return JsonResponse({'status': 'success'})


    # location = Complaint_Statement.objects.get(id=pk)
    # location.latitute = request.POST.get('latitude')
    # location.longitude = request.POST.get('longitude')
    # location.save()
    # return render(request, 'taxiapp/empty.html')

def get_taxi_location(request, pk):
    location = Complaint_Statement.objects.get(id=pk)
    return render(request, 'taxiapp/get_taxi_location.html', {'location': location})


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

def handle_taxi_xlsx(file_path,city, user_number):
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
        owner_vehicle_df = pd.read_excel(s3_object.get()['Body'],sheetname="Vehicle_Owner")
        driver_df = pd.read_excel(s3_object.get()['Body'],sheetname="Driver")
        owner_vehicle_data = owner_vehicle_df.replace(np.nan, '', regex=True)
        driver_data = driver_df.replace(np.nan, '', regex=True)
        if ( len(owner_vehicle_headers) == len(owner_vehicle_data.columns) and len(driver_headers) == len(driver_data.columns)) :
            for ov_column,dvr_column in zip(owner_vehicle_data.columns,driver_data.columns):
                if ( ov_column not in owner_vehicle_headers or dvr_column not in driver_headers ):
                    print(ov_column,dvr_column)
                    s3_object.delete()
                    return ["xlsx_header_error"]
        else :
            s3_object.delete()
            return ["xlsx_header_error"]
    except Exception as e:
        print(e.message)
        s3_object.delete()
        return ["xlsx_file_error"]

    """code to insert First Sheet named - Vehicle_Owner  into Vehicle and Owner Tables"""
    rowNumber = 1
    # vehicleQrCodeList = []
    for index,row in owner_vehicle_data.iterrows():
        rowNumber+=1
        try:                                                                          
            c = City_Code.objects.get(pk=city)
            if (len(row["Traffic Number (13)"]) > 3) or (row["Traffic Number (13)"] in ['','-']):
                # active = Active.objects.get(active_name = "active") 
                active = Active.objects.get(active_name__iexact = "active") 
                owner = Owner(owner_name=row["Owner Name (40)"],address=row["ADDRESS (200)"],date_of_birth=convertToDate(row["DOB (DD/MM/YYYY)"]),son_of=row['Father Name (40)'],phone_number=row['Phone (10)'],aadhar_number=row['Aadhaar (12)'],owner_image_name=row["Owner Image Name (30)"],blood_group=row["Blood Group (3)"],dl_number = row["DL Number (20)"],dl_expiry= convertToDate(row["DL Expiry (DD/MM/YYYY)"]),active = active, created_by = user_number, modified_by = user_number)
                if(owner.owner_image_name is not None and owner.owner_image_name != ''):
                    owner.owner_image = 'images/owners/'+owner.owner_image_name
                owner.save()   
                import datetime  
                vehicle = Vehicle(created_time=datetime.datetime.now(),number_plate=row["Vehicle Number (12)"],traffic_number=row["Traffic Number (13)"],vehicle_make=row["Vehicle Make (20)"],vehicle_model=row["Vehicle Model (20)"],insurance = convertToDate(row["Insurance Date (DD/MM/YYYY)"]),insurance_provider=row["Insurance provider (20)"], insurance_number=row["Insurance number (30)"],autostand=row["Auto Stand (40)"],union=row["Union (40)"],capacity_of_passengers=row["Capacity (2)"],pollution=convertToDate(row["Pollution (DD/MM/YYYY)"]),engine_number=row["Engine Number (20)"],chasis_number=row["Chassis Number (25)"],mfg_date=convertToDate(row["Mfg Date (DD/MM/YYYY)"]),rc_expiry=convertToDate(row["RC Expiry (DD/MM/YYYY)"]),city=c,owner = owner, created_by = user_number, modified_by = user_number)
                vehicle.save()
                # vehicleQrCodeList.append(vehicle.qr_code)
                
        except Exception as e:
            print('Owner and Vehicle save: ',e.message)
            all_errors.append(rowNumber)
            #s3_object.delete()
            #return all_errors
    # downloadVehicleQrcodes(vehicleQrCodeList)
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
                active = Active.objects.get(active_name__iexact = "active")
                driver = Driver(driver_name = row['Driver Name (40)'],address=row['Address (200)'],date_of_birth = convertToDate(row['DOB (DD/MM/YYYY)']),son_of = row['Father Name (40)'],phone_number=row['Phone (10)'], aadhar_number = row['Aadhaar (12)'],dl_number=row['DL Number (20)'],dl_expiry = convertToDate(row['DL Expiry (DD/MM/YYYY)']),driver_image_name=row['Driver Image Name (30)'],vehicle=vehicle,blood_group=row["Blood Group (3)"],active=active, created_by = user_number, modified_by = user_number)
                if(driver.driver_image_name is not None and driver.driver_image_name != ''):
                    driver.driver_image = 'images/drivers/'+driver.driver_image_name
                driver.save()
        except Exception as e:
            print('Driver save: ',e.message)
            all_errors.append(rowNumber)
            #s3_object.delete()
            #return all_errors

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
                    errors = handle_taxi_xlsx(request.FILES['taxi_csv'], request.POST["city"], request.user.user_number)
                    print(errors)
                    if len(errors)==0:
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.\n','message2':''})
                    elif errors[0] == "xlsx_header_error":  
                         return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Invalid file headers to upload. Please Re-Validate and try again. \n','message2':''})     
                    elif errors[0] == "xlsx_file_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File not of type xlsx. Only xlsx files are accepted at the moment.\n','message2':''})
                    elif errors[0] == "network_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Network error during file upload. Please try again.\n','message2':''})                          
                    return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.','message2':'Row Number(s) '+ str((errors)) +' has invalid/duplicate data and they were NOT UPLOADED.'})
            else:
                form = TaxiDetailCsvUpload()
            return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':message})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_csv_upload")


# def bulk_image_upload(request):
#     message = 'Please Upload the Bulk Image ZIP here'
#     secondary_message = 'The images in the zip should be named according to their traffic numbers'
#     if request.user.is_authenticated():
#         if request.user.is_admin or request.user.is_staff:
#             if request.method == "POST":
#                 form = BulkImageUpload(request.POST, request.FILES)
#                 if form.is_valid():
#                     errors = handle_bulk_image_zip(request.FILES['bulk_image_zip'])
#                     if len(errors)==0:
#                         return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':'Files Uploaded Successfully\n','message2':''})
#                     elif errors[0] == "network_error":
#                         return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Network error during file upload. Please try again.\n','message2':secondary_message})  

#                     return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':'Files Uploaded Successfully','message2':str(len(errors))+' were NOT UPLOADED because of invalid filename.'})
#             else:
#                 form = BulkImageUpload()
#             return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':message, 'message2':secondary_message})
#     else:
#         return HttpResponseRedirect("/admin_login?next=bulk_image_upload")

def bulk_image_upload(request):
    if request.user.is_authenticated():
        if request.user.is_admin or request.user.is_staff:
            return render(request, 'taxiapp/bulk_image_upload.html')
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
                 m = send_sms(str(otp_code)+" is your OTP for resetting password",phone_number,'otp'  +'\n'+ 'VALVDATA') 
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
    # customerRating.created_by = request.user.user_number
    customerRating.active = Active.objects.get(active_name__iexact = 'active')
    customerRating.created_by =passenger_phone
    customerRating.created_time = datetime.now()

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
    vehicle_types=Vehicle_type.objects.all()
    sources=Source.objects.all()
    return render(request,'taxiapp/vehicle_registration.html',{'sources':sources,'vehicle_types':vehicle_types})

# def Vehicle_Register_Details(request):
#     traffic_number=request.POST.get('traffic_number')
#     number_plate=request.POST.get('number_plate')
#     autostand=request.POST.get('autostand')
#     insurance=request.POST.get('insurance')
#     union=request.POST.get('union')
#     pollution=request.POST.get('pollution')
#     engine_number=request.POST.get('engine_number')
#     chasis_number=request.POST.get('chasis_number')
#     rc_expiry=request.POST.get('rc_expiry')
#     rc_number=request.POST.get('rc_number')
#     num_of_complaints=0
    
#     active = Active.objects.get(active_name__iexact = 'Inactive')
#     #Set city code object by getting from table
#     city_code =request.POST.get('city_code')
#     city = City_Code.objects.get(city_code=city_code)
#     vehicle_type = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
#     # created_by=''
#     # modified_by=''
#     capacity_of_passengers=request.POST.get('capacity_of_passengers')
#     Owner_name =request.POST.get('Owner_name')
   
#     Owner_Phone_no =request.POST.get('Owner_Phone_no')

#     v1=Vehicle_Registration(traffic_number=traffic_number,number_plate=number_plate,autostand=autostand,
#     insurance=insurance,union=union,pollution=pollution,engine_number=engine_number,chasis_number=chasis_number,
#     rc_expiry=rc_expiry,rc_number=rc_number,num_of_complaints=num_of_complaints,created_by=Owner_name,
#     modified_by=Owner_name,active=active,city=city,vehicle_type=vehicle_type,
#     capacity_of_passengers=capacity_of_passengers)
#     v1.save() 
#     #Send SMS which you captured owner name and PH No
#     message = 'Hi ' + str(Owner_name) + '\nVehicle Registration is Success.'
#     m = send_sms(message,Owner_Phone_no,'complaint')
#     return HttpResponseRedirect("/?message=successfully registered.")

def Add_Vehicle(request):
    vehicleId = request.POST.get('vehicleId')
    drivers = []
    vehicle = Vehicle(
        traffic_number="",
        number_plate="",
        autostand="",
        insurance="",
        union="",
        pollution="",
        engine_number="",
        chasis_number="",
        rc_expiry="",
        num_of_complaints="",
        #active = active
        #city = vehicleregistration.city
        #vehicle_type = vehicleregistration.vehicle_type
        capacity_of_passengers=""
    )
    owner = Owner(owner_name = "",
      address = "",
      date_of_birth = "",
      son_of = "",
      phone_number = "",
      aadhar_number = "",
      blood_group = "",
      dl_number = "",
      dl_expiry = "")
    if(vehicleId is not None) :
        vehicle = Vehicle.objects.get(id = vehicleId)
        owner = vehicle.owner
        drivers = Driver.objects.filter(vehicle = vehicle)
    #cities = City_Code.objects.values_list('city', flat=True).distinct()
    cities = City_Code.objects.all()
    vehice_type=Vehicle_type.objects.values_list('vehicle_type', flat=True).distinct()
    return render(request,'taxiapp/add_vehicle.html',{'cities':cities,'vehice_type':vehice_type,
    'vehicle':vehicle,'owner':owner,'drivers':drivers})

def Register_Vehicle(request):
    vrId = request.POST.get('vrId')
    drivers = []
    vehicle = Vehicle()
    owner = Owner(owner_name = "",
      address = "",
      date_of_birth = "",
      son_of = "",
      phone_number = "",
      aadhar_number = "",
      blood_group = "",
      dl_number = "",
      dl_expiry = "")
    
    if(vrId is not None) :
        vehicleregistration = Vehicle_Registration.objects.get(id = vrId)
        #vehicle.traffic_number=vehicleregistration.traffic_number
        vehicle.number_plate=vehicleregistration.vehicle_number
        vehicle.vehicle_type = vehicleregistration.vehicle_type
        #vehicleregistration.registered = True
        #vehicleregistration.save()
        vehicle.autostand=""
        vehicle.insurance=""
        vehicle.union=""
        vehicle.pollution=""
        vehicle.engine_number=""
        vehicle.chasis_number=""
        vehicle.rc_expiry=""
        vehicle.num_of_complaints=""
        active = Active.objects.get(active_name__iexact = 'Active')
        vehicle.active = active
        #vehicle.city = vehicleregistration.city
        vehicle.vehicle_type = vehicleregistration.vehicle_type
        vehicle.capacity_of_passengers=""

    #cities = City_Code.objects.values_list('city', flat=True).distinct()
    cities = City_Code.objects.all()
    vehice_type=Vehicle_type.objects.values_list('vehicle_type', flat=True).distinct()
    return render(request,'taxiapp/add_vehicle.html',{'cities':cities,'vehice_type':vehice_type,
    'vehicle':vehicle,'owner':owner,'drivers':drivers,'regFlag':True})

def Delete_Vehicle(request):
    vehicleId = request.POST.get('vehicleId')
    vehicle = Vehicle.objects.get(id = vehicleId)
    vehicle.modified_by = request.user.user_number
    vehicle.modified_time = datetime.now()
    active = Active.objects.get(active_name__iexact = 'Inactive')
    vehicle.active = active
    vehicle.save()
    return HttpResponseRedirect("/vehicle_list?message=Successfully deleted.") 

def Delete_Complaint(request):
    complaintId = request.POST.get('complaintId')
    complaint = Complaint_Statement.objects.get(id = complaintId)
    complaint.active = Active.objects.get(active_name__iexact = 'Inactive')
    complaint.save()
    return HttpResponseRedirect("/complaints_list?message=Successfully deleted.")

def Delete_Rating(request):
    ratingId = request.POST.get('ratingId')
    rating = Customer_Rating.objects.get(id = ratingId)
    rating.active = Active.objects.get(active_name__iexact = 'Inactive')
    rating.modified_by = request.user.user_number
    rating.modified_time = datetime.now()
    rating.save()
    return HttpResponseRedirect("/customer_rating_list?message=Successfully deleted.")

def Add_Driver(request):
    vehicle_type=Vehicle_type.objects.values_list('vehicle_type', flat=True).distinct()
    return render(request,'taxiapp/add_driver.html',{'vehicle_type':vehicle_type})

def Add_Vehicle_Details(request):
    #print(request.POST)
    active = Active.objects.get(active_name__iexact = 'active')

    ownerId = request.POST.get('ownerId')
    if(ownerId is not None and ownerId != '' and ownerId != 'None'):
        owner = Owner.objects.get(id=ownerId)
        owner.modified_by = request.user.user_number
        owner.modified_time = datetime.now()
    else :
        owner = Owner()
        owner.created_by = request.user.user_number
        owner.created_time = datetime.now()
    #Read Owner Details
    owner.owner_name = request.POST.get('o_owner_name')
    owner.address = request.POST.get('o_address')
    owner.date_of_birth =convertToDate(request.POST.get('o_date_of_birth'))
    owner.son_of =request.POST.get('o_son_of')
    owner.phone_number =request.POST.get('o_phone_number')
    owner.aadhar_number =request.POST.get('o_aadhar_number')
    owner.dl_number =request.POST.get('o_dl_number')
    owner.dl_expiry =convertToDate(request.POST.get('o_dl_expiry'))
    owner.active = active
    owner.save()
    
    vehicleId = request.POST.get('vehicleId')
    if(vehicleId is not None and vehicleId != '' and vehicleId != 'None'):
        vehicle = Vehicle.objects.get(id=vehicleId)
        vehicle.modified_by = request.user.user_number
        vehicle.modified_time = datetime.now()
    else :
        vehicle = Vehicle()
        vehicle.created_by = request.user.user_number
        vehicle.created_time = datetime.now()
    #Read Vehicle Details
    vehicle.traffic_number=request.POST.get('v_traffic_number')
    vehicle.number_plate=request.POST.get('v_number_plate')
    vehicle.autostand=request.POST.get('v_autostand')
    vehicle.insurance=convertToDate(request.POST.get('v_insurance'))
    vehicle.union=request.POST.get('v_union')
    vehicle.pollution=convertToDate(request.POST.get('v_pollution'))
    vehicle.engine_number=request.POST.get('v_engine_number')
    vehicle.chasis_number=request.POST.get('v_chasis_number')
    vehicle.rc_expiry=convertToDate(request.POST.get('v_rc_expiry'))
    # rc_number=request.POST.get('rc_number')
    vehicle.num_of_complaints=0
    vehicle.active = active
    #Set city code object by getting from table
    city_code =request.POST.get('v_city')
    vehicle.city = City_Code.objects.get(city_code=city_code)
    vehicle.vehicle_type = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    cop = request.POST.get('v_capacity_of_passengers')
    if(cop is not None and cop != '' and cop != 'None'):
        vehicle.capacity_of_passengers = cop
    vehicle.owner = owner
    vehicle.save()

    vehicle_registration = Vehicle_Registration()
    if vehicle.id is not None :
        if ( request.POST.get('regFlag') == True) :
            vehicle_registration = Vehicle_Registration.objects.get(vehicle_number = vehicle.number_plate)
            if len(vehicle_registration) > 0 :
                vehicle_registration.registered = True
                vehicle_registration.save()

    #Read Driver Details
    #traffic_number=request.POST.get('traffic_number')
    driver_Id_list=request.POST.getlist('driverId')
    driver_name_list=request.POST.getlist('d_driver_name')
    address_list=request.POST.getlist('d_address')
    date_of_birth_list=request.POST.getlist('d_date_of_birth')
    son_of_list=request.POST.getlist('d_son_of')
    phone_number_list=request.POST.getlist('d_phone_number')
    aadhar_number_list=request.POST.getlist('d_aadhar_number')
    dl_number_list=request.POST.getlist('d_dl_number')
    dl_expiry_list=request.POST.getlist('d_dl_expiry')
    # deletedDrivers=request.POST.getlist('deletedDrivers')
    # print(deletedDrivers)
    deletedDrivers=request.POST.get('deletedDrivers')
    print(deletedDrivers)
    # vehicle=request.POST.get('vehicles')
    # # vehicle = Vehicle_type.objects.get(vehicle_type__iexact = 'auto')
    if len(driver_name_list) > 0 :
        for (driverId,driver_name,address,date_of_birth,son_of,phone_number,aadhar_number,dl_number,dl_expiry) in zip(
        driver_Id_list, driver_name_list,address_list,date_of_birth_list,son_of_list,phone_number_list,
        aadhar_number_list,dl_number_list,dl_expiry_list) :
            if(driverId is not None and driverId != '' and driverId != 'None'):
                driver = Driver.objects.get(id=driverId)
                driver.modified_by=request.user.user_number
                driver.modified_time=datetime.now()
            else :
                driver = Driver()
                driver.created_by=request.user.user_number
                driver.created_time=datetime.now() 

            driver.driver_name=driver_name
            driver.address=address
            driver.date_of_birth=convertToDate(date_of_birth)
            driver.son_of=son_of
            driver.phone_number=phone_number
            driver.aadhar_number=aadhar_number
            driver.dl_number=dl_number
            driver.dl_expiry=convertToDate(dl_expiry)
            driver.vehicle=vehicle
            driver.active = active
            driver.save()
    if len(deletedDrivers) > 0 :
        driverIds = deletedDrivers.split(',')
        for driverId in driverIds:
            driver = Driver.objects.get(id=driverId)
            driver.modified_by=request.user.user_number
            driver.modified_time=datetime.now()
            driver.vehicle = None
            driver.save()

        # return render(request, 'taxiapp/taxi_list.html', {'message':'successfully \
        # Vehicle added.'})

    return HttpResponseRedirect("/vehicle_list?message=successfully Vehicle added.")
       
    # return render(request, 'taxiapp/add_vehicle.html', {'message':'Unabled to add \
    # Vehicle/Owner/Drivers Details. Please validate input fields and retry'})

def Add_Driver_Details(request):
    driverId = request.POST.get('driverId')
    if(driverId is not None and driverId != '' and driverId != 'None'):
        driver = Driver.objects.get(id=driverId)
        activeTab = 'drivers'
        driver.modified_by=request.user.user_number
        driver.modified_time=datetime.now()
    else :
        driver = Driver()
        activeTab = 'vehicles'
        driver.created_by=request.user.user_number
        driver.created_time=datetime.now()

    active = Active.objects.get(active_name__iexact = 'active')

    driver.driver_name=request.POST.get('driver_name')
    driver.address=request.POST.get('address')
    driver.date_of_birth=convertToDate(request.POST.get('date_of_birth'))
    driver.son_of=request.POST.get('son_of')
    driver.phone_number=request.POST.get('phone_number')
    driver.aadhar_number=request.POST.get('aadhar_number')
    driver.dl_number=request.POST.get('dl_number')
    driver.dl_expiry=convertToDate(request.POST.get('dl_expiry'))
    driver.active = active
    driver.save()
    return HttpResponseRedirect("/driver_list?message=Driver details added successfully.")

def SendSMS_Owner_Driver():
    month = date.today().month
    year = date.today().year
    owners = Owner.objects.filter(dl_expiry__month = month,dl_expiry__year = year)
    for owner in owners :
        try :
            if owner.phone_number is not None and owner.phone_number != '' :
                message = 'Dear '+str(owner.owner_name)+',\n'+'Your Driving License '+str(owner.dl_number)+' is going to expire on '+str(owner.dl_expiry)+'.'
                #m = send_sms(message,owner.phone_number,'complaint')
                print(message)
        except Exception as e:
            print(e.message)
    
    vehicles = Vehicle.objects.filter(rc_expiry__month = month,rc_expiry__year = year)
    for vehicle in vehicles :
        try :
            if vehicle.owner.phone_number is not None and vehicle.owner.phone_number != '' :
                message = 'Dear '+str(vehicle.owner.owner_name)+',\n'+'Your RC for the Vehicle Number'+str(vehicle.number_plate)+' is going to expire on '+str(vehicle.rc_expiry)+'.'
                #m = send_sms(message,vehicle.owner.phone_number,'complaint')
                print(message)
        except Exception as e:
            print(e.message)

    drivers = Driver.objects.filter(dl_expiry__month = month,dl_expiry__year = year)
    for driver in drivers :
        try :
            if driver.phone_number is not None and driver.phone_number != '' :
                message = 'Dear '+str(driver.driver_name)+',\n'+'Your Driving License '+str(driver.dl_number)+' is going to expire on '+str(driver.dl_expiry)+'.'
                #m = send_sms(message,driver.phone_number,'complaint')
                print(message)
        except Exception as e:
            print(e.message)
            
def Delete_Driver(request):
    driverId = request.POST.get('driverId')
    print('driverId',driverId)
    driver = Driver.objects.get(id = driverId)
    active = Active.objects.get(active_name__iexact = 'Inactive')
    driver.modified_by=request.user.user_number
    driver.modified_time=datetime.now()
    driver.active = active
    driver.save()
    return HttpResponseRedirect("/driver_list?message=Successfully deleted.") 

def Disassociate_Driver(request):
    driverId = request.POST.get('driverId')
    print('driverId',driverId)
    driver = Driver.objects.get(id = driverId)
    #active = Active.objects.get(active_name__iexact = 'Inactive')
    driver.modified_by=request.user.user_number
    driver.modified_time=datetime.now()
    vehicle = driver.vehicle
    driver.vehicle = None
    #driver.active = active
    driver.save()
    msg = "Driver "+driver.driver_name+" is disassociated with the vehicle "+vehicle.number_plate+" and Traffic ID "+vehicle.traffic_number
    return HttpResponseRedirect("/driver_list?message="+msg) 
    

def Associate_Driver(request): 
    driverid=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverid)
    active = Active.objects.get(active_name__iexact = 'Active')
    vehicles = Vehicle.objects.filter(active = active )
    return render(request,'taxiapp/associate_driver.html',{'driver':driver,'vehicles':vehicles})

def Associate_VehicleToDriver(request):
    number_plate = request.POST.get('number_plate')
    vehicle = Vehicle.objects.get(number_plate = number_plate)
    driverid=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverid)
    driver.vehicle = vehicle
    driver.modified_by=request.user.user_number
    driver.modified_time=datetime.now()
    driver.save()
    msg = "Driver "+driver.driver_name+" is associated with the vehicle "+vehicle.number_plate+" and Traffic ID "+vehicle.traffic_number
    return HttpResponseRedirect("/driver_list?message="+msg) 

def Vehicle_Register_Details(request):
    #print("Inside Vehicle Reg")
    name = request.POST.get('name')
    vehicleType=request.POST.get('vehicle_type')
    vehicle_type = Vehicle_type.objects.get(vehicle_type__iexact = vehicleType)
    vehicle_number = request.POST.get('vehicle_number')
    phone_number = request.POST.get('phone_number')
    sourceId = request.POST.get('source')
    source = Source.objects.get(id=sourceId)
    # receipt_number = 'AUTO-000001'
    created_by = name
    created_time = datetime.now()
    active = Active.objects.get(active_name__iexact = "active") 
    registered = False
    v1 = Vehicle_Registration(name=name,vehicle_type=vehicle_type,vehicle_number=vehicle_number,
    phone_number=phone_number,source=source,
    created_by=created_by,created_time=created_time,
    active=active,registered=registered)
    v1.save()

    if vehicleType.upper() =='AUTO':
        receipt_number = 'AUTO-'+str(v1.id).zfill(6)
    elif vehicleType.upper() == 'TAXI':
        receipt_number= 'TAXI-'+str(v1.id).zfill(6)
    elif vehicleType.upper() == 'DRIVER':
        receipt_number = 'DRVR-'+str(v1.id).zfill(6)
    else:
        receipt_number = ''
    v1.receipt_number=receipt_number
    v1.save()
    message=" Thanks for registering with SafeAutoTaxi. Your Receipt # is " + str(receipt_number)+ ". Please visit our center and pay Rs.200 to register your vehicle." +'\n'+ 'VALVDATA PRIVATE LIMITED'
    m = send_sms(message,phone_number,'register')   
    return render(request, 'taxiapp/drivers_list.html', {'message':'Vehicle registered successfully with Receipt # is '+str(receipt_number)})
   
def Edit_Driver(request):
    driverId=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverId)
    return render(request,'taxiapp/add_driver.html',{'driver':driver})

# def Allocationlist_Driver(request):
#     #print("Testing..")
#     print(request.POST)
#     print(request.GET)
#     return HttpResponseRedirect("/taxi_list?activeTab=drivers&")

# def Allocationlist_Driver(request):
#     driverid=request.POST.get('drivertId')
#     driver=Driver.objects.get(id=driverid)
#     allocation = request.POST.get('allocation')

#     def Associate_VehicleToDriver(request):
#     number_plate = request.POST.get('number_plate')
#     vehicle = Vehicle.objects.get(number_plate = number_plate)
#     driverid=request.POST.get('driverId')
#     driver=Driver.objects.get(id=driverid)
#     driver.vehicle = vehicle
#     driver.save()
#     msg = "Driver "+driver.driver_name+" is associated with the vehicle "+vehicle.number_plate+" and Traffic ID "+vehicle.traffic_number
#     return HttpResponseRedirect("/taxi_list?message="+msg+".&activeTab=drivers")

def Populate_Numberplate(request):
    traffic_number = request.POST.get('traffic_number')
    number_plate = Vehicle.objects.get(traffic_number = traffic_number).number_plate
    driverid=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverid)
    active = Active.objects.get(active_name__iexact = 'Active')
    vehicles = Vehicle.objects.filter(active = active )
    return render(request,'taxiapp/associate_driver.html',{'driver':driver,'vehicles':vehicles,'number_plate':number_plate,'traffic_number':traffic_number})

def Populate_TrafficNumber(request):
    number_plate = request.POST.get('number_plate')
    traffic_number = Vehicle.objects.get(number_plate = number_plate).traffic_number
    driverid=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverid)
    active = Active.objects.get(active_name__iexact = 'Active')
    vehicles = Vehicle.objects.filter(active = active )
    return render(request,'taxiapp/associate_driver.html',{'driver':driver,'vehicles':vehicles,'number_plate':number_plate,'traffic_number':traffic_number})



def Dashboard(request):
    cities = City_Code.objects.all()
    vehicletypes = Vehicle_type.objects.order_by('vehicle_type').values_list('vehicle_type',flat=True).distinct()
    
    if request.user.is_authenticated():
        city_code = None
        city = None
        vehicletype = request.POST.get('vehicletype')
  
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
            dashboardDict = getDashboardData(None)
            weeklyDashboardDict = getDashboardDataWeekly(None)
        else :
            rows = Vehicle.objects.select_related().filter(city = city)
            city = City_Code.objects.get(city_code = city_code)
            dashboardDict = getDashboardData(city)
            weeklyDashboardDict = getDashboardDataWeekly(city)
        
        dashboardList = []
        weeklydashboardList = []

        if(vehicletype is not None and vehicletype != 'All'):
            vcltype = Vehicle_type.objects.get(vehicle_type = vehicletype)
            dashboardList.append(setDashboardsCounts(dashboardDict,vcltype))
            weeklydashboardList.append(setweeklyDashboardsCounts(weeklyDashboardDict,vcltype))

        else :
            vehicletype = 'All'
            vehicleTypes = Vehicle_type.objects.all()
           
            for vcltype in vehicleTypes :
                dashboardList.append(setDashboardsCounts(dashboardDict,vcltype))
                weeklydashboardList.append(setweeklyDashboardsCounts(weeklyDashboardDict,vcltype))
            dashboardList.append(setDashboardsCounts(dashboardDict,'All'))
            weeklydashboardList.append(setweeklyDashboardsCounts(weeklyDashboardDict,'All'))

        currentDate = datetime.now().date()
        dateList = [currentDate,currentDate-timedelta(days=1),currentDate-timedelta(days=2),currentDate-timedelta(days=3),currentDate-timedelta(days=4),currentDate-timedelta(days=5),currentDate-timedelta(days=6)]
        
        for j in weeklydashboardList :
            if ( j['day0'] == 0 ) :
                j['day0'] = '-'
            if ( j['day1'] == 0 ) :
                j['day1'] = '-'
            if ( j['day2'] == 0 ) :
                j['day2'] = '-'
            if ( j['day3'] == 0 ) :
                j['day3'] = '-'
            if ( j['day4'] == 0 ) :
                j['day4'] = '-'
            if ( j['day5'] == 0 ) :
                j['day5'] = '-'
            if ( j['day6'] == 0 ) :
                j['day6'] = '-'
            if ( j['total'] == 0 ) :
                j['total'] = '-'


        return render(request,'taxiapp/dashboard.html',{
        'cities':cities,'vehicletypes':vehicletypes,'dashboardList':dashboardList, 
        'vehicletype':vehicletype,'city_code':city_code,
        'user':request.user,'weeklydashboardList':weeklydashboardList,'dateList':dateList})
        #'weeklyDataListHeders':weeklyDataListHeders,
    else:
        return HttpResponseRedirect("/admin_login?next=dashboard")

def setDashboardsCounts(dashboardDict,vcltype) :
    vclDashboardDict = {}
    if vcltype == 'All':
        newDashboardDict = getDashboardDataVehicleType(dashboardDict,None)
        vclDashboardDict.update(vehicletype = 'All')
    else :
        newDashboardDict = getDashboardDataVehicleType(dashboardDict,vcltype)
        vclDashboardDict.update(vehicletype = vcltype.vehicle_type)

    todayVR = newDashboardDict['todayVR']
    vclDashboardDict.update(todayVR= len(todayVR))

    thisWeekVR = newDashboardDict['thisWeekVR']
    vclDashboardDict.update(thisWeekVR= len(thisWeekVR))

    thisMonthVR = newDashboardDict['thisMonthVR']
    vclDashboardDict.update(thisMonthVR= len(thisMonthVR))

    thisYearVR = newDashboardDict['thisYearVR']
    vclDashboardDict.update(thisYearVR= len(thisYearVR))

    total = newDashboardDict['total']
    vclDashboardDict.update(total= len(total))
    return vclDashboardDict

def setweeklyDashboardsCounts(dashboardDict,vcltype) :
    vclDashboardDict = {}
    if vcltype == 'All':
        newDashboardDict = getWeeklyDashboardDataVehicleType(dashboardDict,None)
        vclDashboardDict.update(vehicletype = 'All')
    else :
        newDashboardDict = getWeeklyDashboardDataVehicleType(dashboardDict,vcltype)
        vclDashboardDict.update(vehicletype = vcltype.vehicle_type)

    day0 = newDashboardDict['day0']
    vclDashboardDict.update(day0= len(day0))

    day1 = newDashboardDict['day1']
    vclDashboardDict.update(day1= len(day1))
    
    day2 = newDashboardDict['day2']
    vclDashboardDict.update(day2= len(day2))

    day3 = newDashboardDict['day3']
    vclDashboardDict.update(day3= len(day3))

    day4 = newDashboardDict['day4']
    vclDashboardDict.update(day4= len(day4))

    day5 = newDashboardDict['day5']
    vclDashboardDict.update(day5= len(day5))

    day6 = newDashboardDict['day6']
    vclDashboardDict.update(day6= len(day6))

    total = newDashboardDict['total']
    vclDashboardDict.update(total= len(total))
    return vclDashboardDict

def Vehicles_List(request):
    page = 1
    if request.method == "GET":
        page = request.GET.get('page', 1)
    else:
        page = request.POST.get('page', 1)
    message = request.GET.get('message','')  
    cities = []
    if request.user.is_admin or request.user.is_staff:
        cities = City_Code.objects.all()
    else:
        cities.append(request.user.city)

    vehicletypes = Vehicle_type.objects.order_by('vehicle_type').values_list('vehicle_type',flat=True).distinct()
    
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
        else :
            rows = Vehicle.objects.select_related().filter(city = city)

        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            rows = rows.filter(vehicle_type=vehicle_type)
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
            rows = rows.filter(traffic_number__in = rangeList)
        else :
            rangeFrom = ""
            rangeTo = ""
        if (taxiIds is not None and taxiIds != ''):
            taxiIdsArray = taxiIds.split(',')
            rows = rows.filter(traffic_number__in = taxiIdsArray)
        else :
            taxiIds = ""
        if (numberPlates is not None and numberPlates != ''):
            numberPlatesArray = numberPlates.split(',')
            rows = rows.filter(number_plate__in = numberPlatesArray)            
        else :
            numberPlates = ""

        paginator = Paginator(rows, 10)            
        try:
            rowPages = paginator.page(page)
        except PageNotAnInteger:
            rowPages = paginator.page(1)
        except EmptyPage:
            rowPages = paginator.page(paginator.num_pages)
        return render(request,'taxiapp/vehicle_list.html',{'rows':rowPages,
        'cities':cities,'vehicletypes':vehicletypes, 
        'vehicletype':vehicletype,'rangeFrom':rangeFrom,'city_code':city_code,'numberPlates':numberPlates,
        'rangeTo':rangeTo,'taxiIds':taxiIds,
        'user':request.user,'message':message})
    else:
        return HttpResponseRedirect("/admin_login?next=vehicle_list")
     
def Driver_List(request):
    if request.method == "GET":
        allocation_type = request.GET.get('allocation_type','Not_Allocated')
    else:
        allocation_type = request.POST.get('allocation_type', 'Not_Allocated')

    message = request.GET.get('message','')    
    if request.user.is_authenticated():
        if allocation_type == 'Not_Allocated':
            drivers = Driver.objects.filter(vehicle__isnull=True)
        elif allocation_type == 'Allocated':
            drivers = Driver.objects.filter(vehicle__isnull=False)
        else:
            drivers = Driver.objects.all()

        return render(request,'taxiapp/drivers.html',{'drivers':drivers,'message':message,'allocation_type':allocation_type})
    else:
        return HttpResponseRedirect("/admin_login?next=driver_list")


def Complaints_List(request):

    if request.method == "GET":
        resolved_type = request.GET.get('resolved_type','UnResolved')
    else:
        resolved_type = request.POST.get('resolved_type', 'UnResolved')
    
    message = request.GET.get('message','')
    cities = []
    if request.user.is_admin or request.user.is_staff:
        cities = City_Code.objects.all()
    else:
        cities.append(request.user.city)
    vehicletypes = Vehicle_type.objects.order_by('vehicle_type').values_list('vehicle_type',flat=True).distinct()
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
            rows_c = Complaint_Statement.objects.select_related('vehicle')
        else :
            rows_c = Complaint_Statement.objects.filter(city=city)
        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            rows_c = rows_c.filter(vehicle__vehicle_type=vehicle_type)
        else :
            vehicletype = 'All'   
        if (rangeFrom is not None and  rangeFrom != '' and rangeTo is not None and rangeTo != ''):
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
            rows_c=rows_c.filter(vehicle__traffic_number__in = rangeList)
        else :
            rangeFrom = ""
            rangeTo = ""
        if (taxiIds is not None and taxiIds != ''):
            taxiIdsArray = taxiIds.split(',')
            rows_c=rows_c.filter(vehicle__traffic_number__in = taxiIdsArray)
        else :
            taxiIds = ""
        if (numberPlates is not None and numberPlates != ''):
            numberPlatesArray = numberPlates.split(',')
            rows_c=rows_c.filter(vehicle__number_plate__in = numberPlatesArray)
        else :
            numberPlates = ""

        if resolved_type == 'UnResolved':
            rows_c=rows_c.filter(resolved=False)
        elif resolved_type == 'Resolved':
            rows_c=rows_c.filter(resolved=True)
        rows_c=rows_c.exclude(active_id=2)
        
        return render(request,'taxiapp/complaints.html',{'rows_c':rows_c,'cities':cities,'vehicletypes':vehicletypes,
        'vehicletype':vehicletype,'rangeFrom':rangeFrom,'numberPlates':numberPlates,'resolved_type':resolved_type,
        'user':request.user,'message':message})
    else:
        return HttpResponseRedirect("/admin_login?next=complaints_list")

def Customer_Rating_List(request):
    cities = []
    if request.user.is_admin or request.user.is_staff:
        cities = City_Code.objects.all()
    else:
        cities.append(request.user.city)
    vehicletypes = Vehicle_type.objects.order_by('vehicle_type').values_list('vehicle_type',flat=True).distinct()
    message = request.GET.get('message','')    
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
            ratings = Customer_Rating.objects.select_related('vehicle')
        else :
            ratings = Customer_Rating.objects.filter(vehicle__city = city)

        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            ratings = ratings.filter(vehicle__vehicle_type=vehicle_type)
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
                ratings=ratings.filter(vehicle__traffic_number__in = rangeList)
        else :
            rangeFrom = ""
            rangeTo = ""
        if (taxiIds is not None and taxiIds != ''):
            taxiIdsArray = taxiIds.split(',')
            ratings=ratings.filter(vehicle__traffic_number__in = taxiIdsArray)
        else :
            taxiIds = ""
        if (numberPlates is not None and numberPlates != ''):
            numberPlatesArray = numberPlates.split(',')
            ratings=ratings.filter(vehicle__number_plate__in = numberPlatesArray)
        else :
            numberPlates = ""
        return render(request,'taxiapp/customer_rating_list.html',{'ratings':ratings,'cities':cities,
        'vehicletype':vehicletype,'rangeFrom':rangeFrom,'numberPlates':numberPlates,
        'rangeTo':rangeTo,'taxiIds':taxiIds,'vehicletypes':vehicletypes,
        'user':request.user,'message':message})
    else:
        return HttpResponseRedirect("/admin_login?next=customer_rating_list")

def Vehicle_Registration_List(request):
    message = request.GET.get('message','')    
    if request.user.is_authenticated():
        active = Active.objects.get(active_name__iexact = 'Active')
        vehicleregistrations=Vehicle_Registration.objects.filter(active=active, registered = False)
        return render(request,'taxiapp/vehicle_registration_list.html',{'vehicleregistrations': vehicleregistrations,
        'user':request.user,'message':message})
    else:
        return HttpResponseRedirect("/admin_login?next=vehicle_registration_list")

# def Drivers_Export_To_Csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="Drivers.csv"'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8'))
#     writer.writerow([
#         smart_str(u"Traffic Number"),
#         smart_str(u"Number Plate"),
#         smart_str(u"Driver Name"),
#         smart_str(u"Address"),
#         smart_str(u"Date Of Birth"),
#         smart_str(u"Son Of"),
#         smart_str(u"Phone Number"),
#         smart_str(u"Aadhar Number"),
#         smart_str(u"DL Number"),
#         smart_str(u"DL Expiry"),
#         smart_str(u"Driver Image"),
#         smart_str(u"Driver Image Name"),
#         smart_str(u"Created By"),
#         smart_str(u"Created Time"),
#         smart_str(u"Modified By"),
#         smart_str(u"Modified Time"),
#         smart_str(u"Active Name"),
#         smart_str(u"Trafic Number"),
#         smart_str(u"Blood Group"),
#         smart_str(u"Is Image Verified"),
#         # smart_str(u"vehicle_make"),  
#     ])

#     allocation_type = request.POST.get('allocation_type')
#     if request.user.is_authenticated():        
#         if allocation_type == 'Not_Allocated':
#             drivers = Driver.objects.filter(vehicle__isnull=True)
#         elif allocation_type == 'Allocated':
#             drivers = Driver.objects.filter(vehicle__isnull=False)
#         else:
#             drivers = Driver.objects.all()

#         for driver in drivers:
#             if Vehicle is not None:
#                 print(driver)
#                 writer.writerow([
#                     # smart_str(driver.vehicle.traffic_number),
#                     # smart_str(driver.vehicle.number_plate),
#                     smart_str(driver.vehicle.traffic_number),
#                     smart_str(''),
#                     smart_str(driver.driver_name),
#                     smart_str(driver.address),
#                     smart_str(driver.date_of_birth),
#                     smart_str(driver.son_of),
#                     smart_str(driver.phone_number),
#                     smart_str(driver.aadhar_number),
#                     smart_str(driver.dl_number),
#                     smart_str(driver.dl_expiry),
#                     smart_str(driver.driver_image),
#                     smart_str(driver.driver_image_name),
#                     smart_str(driver.created_by),
#                     smart_str(driver.created_time),
#                     smart_str(driver.modified_by),
#                     smart_str(driver.modified_time),
#                     smart_str(driver.active),
#                     smart_str(driver.traffic_number),
#                     smart_str(driver.blood_group),
#                     smart_str(driver.is_image_verified),
#                 ])
#         return response

#     return HttpResponseRedirect("/admin_login?next=driver_list")


def Drivers_Export_To_Csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Drivers.csv"'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Traffic Number"),
        smart_str(u"Number Plate"),
        smart_str(u"Driver Name"),
        smart_str(u"Address"),
        smart_str(u"Date Of Birth"),
        smart_str(u"Son Of"),
        smart_str(u"Phone Number"),
        smart_str(u"Aadhar Number"),
        smart_str(u"DL Number"),
        smart_str(u"DL Expiry"),
        smart_str(u"Driver Image"),
        smart_str(u"Driver Image Name"),
        smart_str(u"Created By"),
        smart_str(u"Created Time"),
        smart_str(u"Modified By"),
        smart_str(u"Modified Time"),
        smart_str(u"Active Name"),
        smart_str(u"Trafic Number"),
        smart_str(u"Blood Group"),
        smart_str(u"Is Image Verified"),
        # smart_str(u"vehicle_make"),  
    ])

    allocation_type = request.POST.get('allocation_type')
    if request.user.is_authenticated():  
        print(allocation_type)      
        if allocation_type == 'Not_Allocated':
        
            drivers = Driver.objects.filter(vehicle__isnull=True)
        elif allocation_type == 'Allocated':
            drivers = Driver.objects.filter(vehicle__isnull=False)
        else:
            drivers = Driver.objects.all()

        for driver in drivers:
            vehicle=driver.vehicle
            if vehicle is not None:
                writer.writerow([
                    smart_str(vehicle.traffic_number),
                    smart_str(vehicle.number_plate),
                    # smart_str(''),
                    # smart_str(''),
                    smart_str(driver.driver_name),
                    smart_str(driver.address),
                    smart_str(driver.date_of_birth),
                    smart_str(driver.son_of),
                    smart_str(driver.phone_number),
                    smart_str(driver.aadhar_number),
                    smart_str(driver.dl_number),
                    smart_str(driver.dl_expiry),
                    smart_str(driver.driver_image),
                    smart_str(driver.driver_image_name),
                    smart_str(driver.created_by),
                    smart_str(driver.created_time),
                    smart_str(driver.modified_by),
                    smart_str(driver.modified_time),
                    smart_str(driver.active),
                    smart_str(driver.traffic_number),
                    smart_str(driver.blood_group),
                    smart_str(driver.is_image_verified),
                ])
            else :
                writer.writerow([
                    # smart_str(vehicle.traffic_number),
                    # smart_str(vehicle.number_plate),
                    smart_str('None'),
                    smart_str('None'),
                    smart_str(driver.driver_name),
                    smart_str(driver.address),
                    smart_str(driver.date_of_birth),
                    smart_str(driver.son_of),
                    smart_str(driver.phone_number),
                    smart_str(driver.aadhar_number),
                    smart_str(driver.dl_number),
                    smart_str(driver.dl_expiry),
                    smart_str(driver.driver_image),
                    smart_str(driver.driver_image_name),
                    smart_str(driver.created_by),
                    smart_str(driver.created_time),
                    smart_str(driver.modified_by),
                    smart_str(driver.modified_time),
                    smart_str(driver.active),
                    smart_str(driver.traffic_number),
                    smart_str(driver.blood_group),
                    smart_str(driver.is_image_verified),
                ])
        return response

    return HttpResponseRedirect("/admin_login?next=driver_list")


# def Vehicle_Export_To_Csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="Vehicles.csv"'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8'))
#     writer.writerow([
#             smart_str(u"Traffic Number"),
#             smart_str(u"Number Plate"),
#             smart_str(u"Autostand"),
#             smart_str(u"Union"),
#             smart_str(u"Insurance"),
#             smart_str(u"Capacity Of Passengers"),
#             smart_str(u"Pollution"),
#             smart_str(u"Engine Number"),
#             smart_str(u"Chasis Number"),
#             smart_str(u"Is Owner Driver"),
#             smart_str(u"Created By"),
#             smart_str(u"Created Time"),
#             smart_str(u"Modified By"),
#             smart_str(u"Modified Time"),
#             smart_str(u"Active"),
#             smart_str(u"City"),
#             smart_str(u"Owner Name"),
#             smart_str(u"Vehicle Type"),
#             smart_str(u"Num Of Complaints"),
#             smart_str(u"Vehicle Make"),
#             smart_str(u"Vehicle Model"),
#             smart_str(u"Mfg Date"),
#             smart_str(u"Insurance Provider"),
#             smart_str(u"Insurance Number"),
#     ])
    
#     if request.user.is_authenticated():
#         city_code = None
#         city = None
#         vehicletype = request.POST.get('vehicletype')
#         rangeFrom = request.POST.get('rangeFrom')# Last five digits of Traffic Number
#         rangeTo = request.POST.get('rangeTo') # Last five digits of Traffic Number
#         taxiIds = request.POST.get('taxiIds') # Traffic Numbers
#         numberPlates = request.POST.get('numberPlates') # Number Plates
#         if request.user.is_admin:
#             city_code = request.POST.get('city_code')
#             if(city_code is not None and city_code != 'All'):
#                 city = City_Code.objects.get(city_code = city_code)
#             else :
#                 city_code = 'All'
#         else:
#            city = request.user.city
#            city_code = city.city_code
        
#         if (city_code == 'All') :
#             rows = Vehicle.objects.select_related()
#         else :
#             rows = Vehicle.objects.select_related().filter(city = city)

#         if(vehicletype is not None and vehicletype != 'All'):
#             vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
#             rows = rows.filter(vehicle_type=vehicle_type)
#         else :
#             vehicletype = 'All'   
#         if (rangeFrom is not None and  rangeFrom != '' and rangeTo is not None and rangeTo != ''):
#             rangeFromList = rangeFrom.split('-')
#             print(rangeFromList)
#             commonStr = rangeFromList[0]+"-"+rangeFromList[1]
#             rangeLen = len(rangeFromList[2])
#             rangeFromValue = int(rangeFromList[2])
#             rangeDiff = ( int(rangeTo.split('-')[2]) - rangeFromValue ) + 1
#             rangeList = []            
#             for i in range(rangeDiff):
#                 rangFromValuelen = len(str(rangeFromValue))
#                 leadingZero = rangeLen - rangFromValuelen
#                 rangeList.append(commonStr+"-"+str(rangeFromValue).zfill(leadingZero + rangFromValuelen))
#                 rangeFromValue =  rangeFromValue + 1
#             print(rangeList)
#             rows = rows.filter(traffic_number__in = rangeList)
#         else :
#             rangeFrom = ""
#             rangeTo = ""
#         if (taxiIds is not None and taxiIds != ''):
#             taxiIdsArray = taxiIds.split(',')
#             rows = rows.filter(traffic_number__in = taxiIdsArray)
#         else :
#             taxiIds = ""
#         if (numberPlates is not None and numberPlates != ''):
#             numberPlatesArray = numberPlates.split(',')
#             rows = rows.filter(number_plate__in = numberPlatesArray)            
#         else :
#             numberPlates = ""

#         for vehicle in rows:
#             # owner_name = vehicle.owner.owner_name
#             writer.writerow([
#                 smart_str(vehicle.traffic_number),
#                 smart_str(vehicle.number_plate),
#                 smart_str(vehicle.autostand),
#                 smart_str(vehicle.union),
#                 smart_str(vehicle.insurance),
#                 smart_str(vehicle.capacity_of_passengers),
#                 smart_str(vehicle.pollution),
#                 smart_str(vehicle.engine_number),
#                 smart_str(vehicle.chasis_number),
#                 smart_str(vehicle.is_owner_driver),
#                 smart_str(vehicle.created_by),
#                 smart_str(vehicle.created_time),
#                 smart_str(vehicle.modified_by),
#                 smart_str(vehicle.modified_time),
#                 smart_str(vehicle.active),
#                 smart_str(vehicle.city),
#                 smart_str(vehicle.owner),
#                 smart_str(vehicle.vehicle_type),
#                 smart_str(vehicle.num_of_complaints),
#                 smart_str(vehicle.vehicle_make),
#                 smart_str(vehicle.vehicle_model),
#                 smart_str(vehicle.mfg_date),
#                 smart_str(vehicle.insurance_provider),
#                 smart_str(vehicle.insurance_number),
            
#             ])
#         return response

#     return HttpResponseRedirect("/admin_login?next=vehicle_list")


def Vehicle_Export_To_Csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Vehicles.csv"'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
            smart_str(u"Traffic Number"),
            smart_str(u"Number Plate"),
            smart_str(u"Autostand"),
            smart_str(u"Union"),
            smart_str(u"Insurance"),
            smart_str(u"Capacity Of Passengers"),
            smart_str(u"Pollution"),
            smart_str(u"Engine Number"),
            smart_str(u"Chasis Number"),
            smart_str(u"Is Owner Driver"),
            smart_str(u"Created By"),
            smart_str(u"Created Time"),
            smart_str(u"Modified By"),
            smart_str(u"Modified Time"),
            smart_str(u"Active"),
            smart_str(u"City"),
            smart_str(u"Vehicle Type"),
            smart_str(u"Num Of Complaints"),
            smart_str(u"Vehicle Make"),
            smart_str(u"Vehicle Model"),
            smart_str(u"MFG Date"),
            smart_str(u"Insurance Provider"),
            smart_str(u"Insurance Number"),
            smart_str(u"Owner Name"),
            smart_str(u"Address"),
            smart_str(u"Date Of Birth"),
            smart_str(u"Son Of"),
            smart_str(u"Phone Number"),
            smart_str(u"Aadhar Number"),
            smart_str(u"Owner Image"),
            smart_str(u"Owner Image Name"),
            smart_str(u"Blood Group"),
            smart_str(u"DL Number"),
            smart_str(u"DL Expiry"),
            # smart_str(u"Active Name"),
            smart_str(u"Created By"),
            smart_str(u"created_time"),
            smart_str(u"Modified By"),
            smart_str(u"Modified Time"),
            smart_str(u"Is IMage Verified"),
    ])
    
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
        else :
            rows = Vehicle.objects.select_related().filter(city = city)

        if(vehicletype is not None and vehicletype != 'All'):
            vehicle_type = Vehicle_type.objects.get(vehicle_type = vehicletype)
            rows = rows.filter(vehicle_type=vehicle_type)
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
            rows = rows.filter(traffic_number__in = rangeList)
        else :
            rangeFrom = ""
            rangeTo = ""
        if (taxiIds is not None and taxiIds != ''):
            taxiIdsArray = taxiIds.split(',')
            rows = rows.filter(traffic_number__in = taxiIdsArray)
        else :
            taxiIds = ""
        if (numberPlates is not None and numberPlates != ''):
            numberPlatesArray = numberPlates.split(',')
            rows = rows.filter(number_plate__in = numberPlatesArray)            
        else :
            numberPlates = ""

        for vehicle in rows:
            # owner_name = vehicle.owner.owner_name
            owner=vehicle.owner
            # active=owner.active
            if owner is not None:
                # if active is not None:
                    writer.writerow([
                        smart_str(vehicle.traffic_number),
                        smart_str(vehicle.number_plate),
                        smart_str(vehicle.autostand),
                        smart_str(vehicle.union),
                        smart_str(vehicle.insurance),
                        smart_str(vehicle.capacity_of_passengers),
                        smart_str(vehicle.pollution),
                        smart_str(vehicle.engine_number),
                        smart_str(vehicle.chasis_number),
                        smart_str(vehicle.is_owner_driver),
                        smart_str(vehicle.created_by),
                        smart_str(vehicle.created_time),
                        smart_str(vehicle.modified_by),
                        smart_str(vehicle.modified_time),
                        smart_str(vehicle.active),
                        smart_str(vehicle.city),
                        smart_str(vehicle.vehicle_type),
                        smart_str(vehicle.num_of_complaints),
                        smart_str(vehicle.vehicle_make),
                        smart_str(vehicle.vehicle_model),
                        smart_str(vehicle.mfg_date),
                        smart_str(vehicle.insurance_provider),
                        smart_str(vehicle.insurance_number),
                        smart_str(owner.owner_name),
                        smart_str(owner.address),
                        smart_str(owner.date_of_birth),
                        smart_str(owner.son_of),
                        smart_str(owner.phone_number),
                        smart_str(owner.aadhar_number),
                        smart_str(owner.owner_image),
                        smart_str(owner.owner_image_name),
                        smart_str(owner.blood_group),
                        smart_str(owner.dl_number),
                        smart_str(owner.dl_expiry),
                        # smart_str(active.active_name),
                        smart_str(owner.created_by),
                        smart_str(owner.created_time),
                        smart_str(owner.modified_by),
                        smart_str(owner.modified_time),
                        smart_str(owner.is_image_verified),

                ])
        return response

    return HttpResponseRedirect("/admin_login?next=vehicle_list")


def Upload_Images(request):
    message = 'Successfully moved images. '
    all_errors = []
    if request.user.is_authenticated():
        bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
        s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.Bucket(bucketName)
        for key in bucket.objects.filter(Prefix='ImagesDump'):
            filePath = key.key
            object_acl = s3.ObjectAcl(bucketName, filePath)
            response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
            fileName = filePath.split('/')[1]
            if fileName is not None and fileName != '':
                try:                    
                    owner = Owner.objects.get(owner_image_name = fileName)
                    # print('owner: '+owner.owner_image_name)
                    # dest = s3.Bucket(bucketName)
                    source= { 'Bucket' : bucketName, 'Key': str(filePath)}
                    destination = 'images/owners/' + fileName
                    bucket.copy(source, destination)
                    #Grant public Permisions
                    object_acl = s3.ObjectAcl(bucketName, destination)
                    response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
                    #Delete Source
                    key.delete()

                    owner.owner_image = destination
                    owner.is_image_verified = True
                    owner.save()
                except Exception as e:
                    print(e.message)
                    try:
                        driver = Driver.objects.get(driver_image_name = fileName) 
                        # print('driver: '+ driver.driver_image_name)
                        source= { 'Bucket' : bucketName, 'Key': str(filePath)}
                        destination = 'images/drivers/' + fileName
                        bucket.copy(source, destination)
                        #Grant public Permisions
                        object_acl = s3.ObjectAcl(bucketName, destination)
                        response = object_acl.put(ACL = settings.AWS_DEFAULT_ACL)
                        #Delete Source
                        key.delete()

                        driver.driver_image = destination
                        driver.is_image_verified = True
                        driver.save()
                    except Exception as e:
                        print(e.message)
                        all_errors.append(fileName)
                
        if len(all_errors) > 0:
            message = message + str((all_errors)) + ' Not found.'

        return render(request,'taxiapp/bulk_image_upload.html',{'message':message})
        
    else:
        return HttpResponseRedirect("/admin_login?next=bulk_image_upload")


def Delete_Vehicle_Registration(request):
    vrId = request.POST.get('vrId')
    vehicle_register = Vehicle_Registration.objects.get(id = vrId)
    vehicle_register.modified_by = request.user.user_number
    vehicle_register.modified_time = datetime.now()
    active = Active.objects.get(active_name__iexact = 'Inactive')
    vehicle_register.active = active
    vehicle_register.save()
    return HttpResponseRedirect("/vehicle_registration_list?message=Successfully deleted.") 


def Driver_Detail(request, pk):
    if ' ' in pk:
        pk = pk.replace(' ','')
    driver = Driver()
    try:
        driver=Driver.objects.get(id=pk)
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
            # We have setted images/profile.png to avoid erros where qr coeds are not there.
            # Need to modify.
            try:                                
                fileName = str(driver.qr_code)
                if(fileName is not None and fileName != ''):
                    objs = list(bucket.objects.filter(Prefix=fileName))
                    if(len(objs) == 0):
                        driver.qr_code = 'images/profile.png'
                else:
                    driver.qr_code = 'images/profile.png'    
            except Exception as e:
                driver.qr_code = 'images/profile.png'

    except Exception as e:    
        print(e)   
    if(driver.id is not None) :
        print('driver',driver)
        return render(request, 'taxiapp/driver_details.html', {'driver':driver}) 
    else:
        return render(request, 'taxiapp/driver_details_fail.html', {'message':"No driver found with the given Driver Id."})

def Generate_Driver_Qrcodes(request):
    if request.user.is_authenticated():
        drivers=Driver.objects.filter(qr_code ='')
        for driver in drivers:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=0,
            )
            weburl = "https://mytaxisafe.com/driver"
            qr.add_data("%s/%s" % (weburl, str(driver.id)))
            qr.make(fit=True)
            img = qr.make_image()
            buffer = StringIO.StringIO()
            img.save(buffer)
            file_name = secure_filename('%s.png' % driver.id)
            file_buffer = InMemoryUploadedFile(
                buffer, None, file_name, 'image/png', buffer.len, None)
            driver.qr_code.save(file_name, file_buffer)

            driver.modified_by=request.user.user_number
            driver.modified_time=datetime.now()

            driver.save()
        return render(request,'taxiapp/migration.html')
    else:
        return HttpResponseRedirect("/admin_login")

def Download_Vehicle_QRcode(request):
    vehicleId = request.POST.get('vehicleId')
    vehicle = Vehicle.objects.get(id = vehicleId)
    if (vehicle.qr_code is not None and vehicle.qr_code !=''):
        try:
            bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
            qrCode= str(vehicle.qr_code)
            qrCodeName=qrCode.split('/')[2]
            file_Name = "https://"+bucketName+".s3.amazonaws.com/"+qrCode
            r = requests.get(file_Name)
            response= HttpResponse(r.content, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="%s"'% qrCodeName
            return response
        except IOError as e:
            print(e)
            return HttpResponseRedirect("/vehicle_list")            
    return HttpResponseRedirect("/vehicle_list")

def Download_Driver_Qrcode(request):
    driverid=request.POST.get('driverId')
    driver=Driver.objects.get(id=driverid)
    if (driver.qr_code is not None and driver.qr_code !=''):
        try:
            bucketName = constants.BULK_UPLOAD_S3_BUCKETNAME
            qrCode= str(driver.qr_code)
            qrCodeName=qrCode.split('/')[2]
            file_Name = "https://"+bucketName+".s3.amazonaws.com/"+qrCode
            r = requests.get(file_Name)
            response= HttpResponse(r.content, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="%s"'% qrCodeName
            return response
        except IOError as e:
            print(e)
            return HttpResponseRedirect("/driver_list")            
    return HttpResponseRedirect("/driver_list")