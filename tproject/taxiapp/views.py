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
    params = simplejson.dumps({'longUrl': url})
    headers = { 'Content-Type' : 'application/json' }
    req = urllib2.Request('https://www.googleapis.com/urlshortener/v1/url?key='+settings.GOOGLE_URL_SHORTENER_KEY, params, headers)
    f = urllib2.urlopen(req)
    return strip_scheme(simplejson.loads(f.read())['id'])

def home(request):
    if request.method == "POST":
        form = TaxisearchForm(request.POST)
        taxi_id = request.POST.get('taxi_id', '')
        print taxi_id
        return HttpResponseRedirect("/taxi/"+taxi_id)
    else:
        form = TaxisearchForm()
        return render(request, 'taxiapp/drivers_list.html', {'form' : form})



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
    taxi = Taxi_Detail.objects.filter(traffic_number__iexact=pk)
    if len(taxi)<1:
        taxi = Taxi_Detail.objects.filter(number_plate__iexact=pk,owner_driver="Owner")
    if len(taxi)<1:
        taxi = Taxi_Detail.objects.filter(number_plate__iexact=pk)
#    taxi = get_object_or_404(Taxi_Detail, traffic_number=pk)
    if len(taxi) > 0:
        m = taxi[0]
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
        return render(request, 'taxiapp/taxi_detail.html', {'taxi': m})
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
            t = Taxi_Detail.objects.get(id=form.instance.taxi.id)
            t.num_of_complaints = t.num_of_complaints+1
            t.save()
            return HttpResponseRedirect("/complaint_success/"+str(form.instance.complaint_number))
    else:
        taxi_id = request.GET.get('id', '')
        passenger_phone = request.GET.get('passenger_phone','')
        passenger_origin = request.GET.get('passenger_origin','')
        passenger_destination = request.GET.get('passenger_destination','')
        form = ComplaintUserForm(initial={'taxi':taxi_id,'phone_number':passenger_phone,\
               'origin_area':passenger_origin,'destination_area':passenger_destination})
        form.fields['taxi'].widget = forms.TextInput(attrs={'size':'30','readonly':"True"})
    	return render(request, 'taxiapp/complaint.html', {'form': form})

def send_sms(message,phone_number,kind):
    if kind == 'emergency':
        r = requests.get('https://www.smsstriker.com/API/sms.php', params={'username':'ValvDataPvtLtd','password':'T@*1App123','from':'TAXSOS','to':str(phone_number),'msg':str(message),'type':'1'}) 
    elif kind == 'complaint':
        r = requests.get('https://www.smsstriker.com/API/sms.php', params={'username':'ValvDataPvtLtd','password':'T@*1App123','from':'TAXCOM','to':str(phone_number),'msg':str(message),'type':'1'})
    elif kind == 'otp':
        r = requests.get('https://www.smsstriker.com/API/sms.php', params={'username':'ValvDataPvtLtd','password':'T@*1App123','from':'TAXOTP','to':str(phone_number),'msg':str(message),'type':'1'})
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
        complaint.save()
        taxi = Taxi_Detail.objects.get(id=complaint.taxi.id)
        map_url = 'https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''
        message = 'Complaint\n'+'Name: '+str(taxi.driver_name)+'\n'+'Taxi Number: '+str(taxi.number_plate)+'\n'+'Phone Number:'+str(taxi.phone_number)+'\nComplaint Reason: '+str(complaint.complaint)+'\nLocation: '+googl(map_url)+'\nPassenger Phone Number:'+str(complaint.phone_number)+'\nOrigin:'+str(complaint.origin_area)+'\nDestination:'+str(complaint.destination_area)
        if taxi.city.sms:
            m = send_sms(message,phone_number,'complaint')
        if taxi.city.whatsapp:
            m = send_whatsapp(message,whatsapp_number)
    return render(request,'taxiapp/complaint_success.html',{'message1':'Your complaint for Taxi has been successfully registered.','message2':'Complaint Number: '+str(pk)})

def complaint_resolve(request,pk):
    if request.user.is_authenticated():
        row = Complaint_Statement.objects.get(id=pk)
        taxi = row.taxi
        t = Taxi_Detail.objects.get(id=taxi.id)
        t.num_of_complaints = max(0,t.num_of_complaints-1)
        t.save()
        row.resolved = True
        row.save()
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
        reason_statement = ''
        return render(request,'taxiapp/complaint_view.html',{'row':row})
    else:
        return HttpResponseRedirect("/admin_login?next=complaint_view/"+str(pk))

def taxi_list(request):
    if request.user.is_authenticated():
        if request.user.is_admin:
            rows = Taxi_Detail.objects.all()
            rows_c = Complaint_Statement.objects.all()
            return render(request,'taxiapp/taxi_list.html',{'rows_c':rows_c,'rows':rows})
        else:
            city = request.user.city
            rows = Taxi_Detail.objects.filter(city=city)
            rows_c = Complaint_Statement.objects.filter(city=city)
            return render(request,'taxiapp/taxi_list.html',{'rows_c':rows_c,'rows':rows})
    else:
        return HttpResponseRedirect("/admin_login?next=taxi_list")



def get_distance(lat,lon,x,y):
    return (lat-x)**2+(lon-y)**2

def taxi_emergency(request):
    if request.method == "POST":
        rows = MyUser.objects.all()
        point = request.POST.get('point','0,0')
        taxi_id = request.POST.get('id')
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
            taxi = Taxi_Detail.objects.get(id=taxi_id)
            message = 'SOS\n'+'Name: '+str(taxi.driver_name)+'\n'+'Taxi Number: '+str(taxi.number_plate)+'\n'+'Driver Phone Number:'+str(taxi.phone_number)+'\nEmergency SOS\nLocation: '+str(googl('https://www.google.co.in/maps/place/'+str(lat)+','+str(lon)+''))+'\nPassenger Phone Number:'+str(p_phone)+'\nOrigin:'+str(p_origin)+'\nDestination:'+str(p_destination)
            if taxi.city.sms:
                m = send_sms(message,phone_number,'emergency')
            if taxi.city.whatsapp:
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

def handle_taxi_csv(file_path,city):
    import os,numpy as np
    bucketName = settings.BULK_UPLOAD_S3_BUCKETNAME
    headers = ['AUTO NUMBER','TRAFFIC NUMBER','NAME','FATHER NAME','DATE OF BIRTH','PHONE NUMBER','ADDRESS','AADHAR NUMBER','DRIVING LICENSE NUMBER','DATE OF VALIDITY','AUTO STAND','UNION','INSURANCE','CAPACITY OF PASSENGERS','POLLUTION','ENGINE NUMBER','CHASIS NUMBER','OWNERDRIVER','DRIVER IMAGE FILENAME']
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
        s3_data = StringIO(s3_object.get()['Body'].read().decode('utf-8'))
        data = pd.read_csv(s3_data)
        data = data.replace(np.nan, '', regex=True)
        if len(headers) == len(data.columns):
            for column in data.columns:
                if column not in headers:
                    s3_object.delete()
                    return ["csv_header_error"]
        else :
            s3_object.delete()
            return ["csv_header_error"]
    except Exception as e:
        s3_object.delete()
        return ["csv_file_error"]
    rowNumber = 1
    for index,row in data.iterrows(): 
        rowNumber+=1
        try:                                                                          
            c = City_Code.objects.get(pk=city)
            p = Taxi_Detail(number_plate=row["AUTO NUMBER"],traffic_number=row["TRAFFIC NUMBER"],driver_name=row["NAME"],son_of=row["FATHER NAME"],date_of_birth=date_form(row["DATE OF BIRTH"]),phone_number=row["PHONE NUMBER"],address=row["ADDRESS"],aadhar_number=row["AADHAR NUMBER"],driving_license_number=row["DRIVING LICENSE NUMBER"],date_of_validity=date_form(row["DATE OF VALIDITY"]),autostand=row['AUTO STAND'],union=row['UNION'],insurance=date_form(row["INSURANCE"]),capacity_of_passengers=row["CAPACITY OF PASSENGERS"],pollution=date_form(row["POLLUTION"]),engine_number=row["ENGINE NUMBER"],chasis_number=row["CHASIS NUMBER"],owner_driver=row["OWNERDRIVER"],driver_image_name=row["DRIVER IMAGE FILENAME"],city=c)
            if (len(row["TRAFFIC NUMBER"]) > 3) or (row["TRAFFIC NUMBER"] in ['','-']):
                p.save()
        except Exception as e:
            all_errors.append(rowNumber)
    s3_object.delete()
    return all_errors


def handle_bulk_image_zip(file_path):
    import os,zipfile,shutil
    path = '/home/ec2-user/taxiapp/tproject/'
    dest = open(path+"images.zip","wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()
    zip_ref = zipfile.ZipFile(path+"images.zip", 'r')
    try:
        os.mkdir(path+'bulk_tmp')
    except:
        shutil.rmtree(path+'bulk_tmp')
        os.mkdir(path+'bulk_tmp')
    try:
        zip_ref.extractall(path+'bulk_tmp')
    except:
        os.remove(path+"images.zip")
        zip_ref.close()
        shutil.rmtree(path+'bulk_tmp')
        return ["csv_file_error"]
    zip_ref.close()
    os.remove(path+"images.zip")
    all_errors=[]
    for images in os.listdir(path+'bulk_tmp/'+os.listdir(path+'bulk_tmp/')[0]+"/"):
        try:
           full_path = path+'bulk_tmp/'+os.listdir(path+'bulk_tmp/')[0]+"/"+images
           taxis = Taxi_Detail.objects.filter(driver_image_name__contains = images.strip())
           for t in taxis:
               t.driver_image.save("drivers",File(open(full_path)))
               t.save()
        except Exception as e:
            all_errors.append(e)
    print(all_errors)
    shutil.rmtree(path+'bulk_tmp')
    return all_errors



def taxi_csv_upload(request):
    message = 'Please Upload the CSV file here'
    secondary_message = ' The columns should strictly be AUTO NUMBER, TRAFFIC NUMBER, NAME,\nFATHER NAME, DATE OF BIRTH, PHONE NUMBER, ADDRESS, AADHAR NUMBER,\nDRIVING LICENSE NUMBER, DATE OF VALIDITY, AUTO STAND, UNION, INSURANCE,\nCAPACITY OF PASSENGERS, POLLUTION, ENGINE NUMBER, CHASIS NUMBER, OWNERDRIVER, DRIVER IMAGE FILENAME'
    if request.user.is_authenticated():
        if request.user.is_admin or request.user.is_staff:
            if request.method == "POST":
                form = TaxiDetailCsvUpload(request.POST, request.FILES)
                if form.is_valid():
                    errors = handle_taxi_csv(request.FILES['taxi_csv'],request.POST["city"])
                    print(errors)
                    if len(errors)==0:
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.\n','message2':''})
                    elif errors[0] == "csv_header_error":  
                         return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Invalid file headers to upload. Please Re-Validate and try again. \n','message2':''})     
                    elif errors[0] == "csv_file_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File not of type CSV. Only CSV files are accepted at the moment.\n','message2':secondary_message})
                    elif errors[0] == "network_error":
                        return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'Network error during file upload. Please try again.\n','message2':secondary_message})                          
                    # return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.','message2':'Row Number '+ str((errors)) +' duplicates to the previous entries were found in the file and they were NOT UPLOADED'})
                    return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':'File Uploaded Successfully.','message2':'Row Number(s) '+ str((errors)) +' has invalid/duplicate data and they were NOT UPLOADED.'})
            else:
                form = TaxiDetailCsvUpload()
            return render(request, 'taxiapp/taxi_csv_upload.html', {'form': form, 'message1':message, 'message2':secondary_message})
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
                    elif errors[0] == "csv_file_error":
                        return render(request, 'taxiapp/bulk_image_upload.html', {'form': form, 'message1':'ERROR: Files are not images.\n','message2':secondary_message})
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
        
        taxiDetails = Taxi_Detail.objects.all()
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
            taxiDetails = taxiDetails.filter(traffic_number__in = rangeList)
        if (taxiIds != None):
            taxiIdsArray = taxiIds.split(',')
            taxiDetails = taxiDetails.filter(traffic_number__in = taxiIdsArray)
        if (numberPlates != None):
            numberPlatesArray = numberPlates.split(',')
            taxiDetails = taxiDetails.filter(number_plate__in = numberPlatesArray)
        if (cityCode != None):
            taxiDetails = taxiDetails.filter(city__city_code = cityCode)


        paginator = Paginator(taxiDetails, limit)
        try:
            taxiDetails = paginator.page(page)
        except PageNotAnInteger:
            taxiDetails = paginator.page(1)
        except EmptyPage:
            taxiDetails = paginator.page(paginator.num_pages)

        serializer = TaxiDriverOwnerSerialize(taxiDetails,many=True)        
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
            complaints = complaints.filter(taxi__traffic_number__in = rangeList)
        if (taxiIds != None):
            taxiIdsArray = taxiIds.split(',')
            complaints = complaints.filter(taxi__traffic_number__in = taxiIdsArray)
        if (numberPlates != None):
            numberPlatesArray = numberPlates.split(',')
            complaints = complaints.filter(taxi__number_plate__in = numberPlatesArray)
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


