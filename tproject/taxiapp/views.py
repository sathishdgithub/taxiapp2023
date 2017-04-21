from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

client = Client(login='919704807427', password='NNpCqG5QJvmHOaSy3XvyEylCmnY=')

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
        return render(request, 'taxiapp/taxi_detail.html', {'taxi': taxi[0]})
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
        r = requests.get('http://www.smsstriker.com/API/sms.php', params={'username':'ValvDataPvtLtd','password':'T@*1App123','from':'TAXSOS','to':str(phone_number),'msg':str(message),'type':'1'}) 
    elif kind == 'complaint':
        r = requests.get('http://www.smsstriker.com/API/sms.php', params={'username':'ValvDataPvtLtd','password':'T@*1App123','from':'TAXCOM','to':str(phone_number),'msg':str(message),'type':'1'})
    return r

def send_whatsapp(message,phone_number):
    k = client.send_message('91'+str(phone_number), message=message)
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
            print m
        if taxi.city.whatsapp:
            m = send_whatsapp(message,whatsapp_number)
            print m
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
        rows = Taxi_Detail.objects.all()
        rows_c = Complaint_Statement.objects.all()
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

