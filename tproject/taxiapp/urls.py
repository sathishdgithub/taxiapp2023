from django.conf.urls import url
from . import views

app_name = "taxiapp"

urlpatterns = [
	url(r'^$', views.home, name = "home"),
	url(r'^admin_login/', views.admin_login, name = "admin_login"),
	url(r'^drivers_list/', views.drivers_list, name = "drivers_list"),
]