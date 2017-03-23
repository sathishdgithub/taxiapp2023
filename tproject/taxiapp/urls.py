from django.conf.urls import url
from . import views

app_name = "taxiapp"

urlpatterns = [
	url(r'^$', views.home, name = "home"),
	url(r'^admin_login/', views.admin_login, name = "admin_login"),
	url(r'^drivers_list/', views.drivers_list, name = "drivers_list"),
	url(r'^taxi_new/$', views.taxi_new, name='taxi_new'),
	url(r'^taxi/(?P<pk>\d+)/$', views.taxi_detail, name='taxi_detail'),
        url(r'^complaint/(?P<pk>\d+)/$', views.complaint_form, name='complaint_form'),
        url(r'^complaint_success/(?P<pk>\d+)/$', views.complaint_success, name='complaint_success'),
]
