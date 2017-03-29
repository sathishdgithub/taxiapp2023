from django.conf.urls import url
from . import views
from django.conf.urls import handler404

app_name = "taxiapp"

urlpatterns = [
	url(r'^$', views.home, name = "home"),
	url(r'^admin_login/', views.admin_login, name = "admin_login"),
        url(r'^admin_logout/', views.admin_logout, name = "admin_logout"),
#	url(r'^taxi_new/$', views.taxi_new, name='taxi_new'),
	url(r'^taxi/(?P<pk>[\w\-]+)/$', views.taxi_detail, name='taxi_detail'),
        url(r'^complaint/(?P<pk>\d+)/$', views.complaint_form, name='complaint_form'),
        url(r'^complaint_success/(?P<pk>\d+)/$', views.complaint_success, name='complaint_success'),
        url(r'^complaint_list/$', views.complaint_list, name='complaint_list'),
        url(r'^complaint_resolve/(?P<pk>\d+)/$', views.complaint_resolve, name='complaint_resolve'),
        url(r'^complaint_view/(?P<pk>[\w\-]+)/$', views.complaint_view, name='complaint_view'),
        url(r'^taxi_list/$', views.taxi_list, name='taxi_list'),
        url(r'^taxi_emergency/(?P<lat>(\d+(?:\.\d+)?))/(?P<lon>(\d+(?:\.\d+)?))/(?P<taxi_id>\d+)/$', views.taxi_emergency, name='taxi_emergency'),
        url(r'^health_check/$', views.health_check, name='health_check'),

]
handler404 = 'views.handler404'

