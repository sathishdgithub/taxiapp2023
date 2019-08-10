from django.conf.urls import url
from . import views

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from . import swagger

app_name = "taxiapp"

#schema_view = get_swagger_view(title="Swagger Docs")
 

urlpatterns = [
	url(r'^$', views.home, name = "home"),
	url(r'^admin_login/', views.admin_login, name = "admin_login"),
        url(r'^admin_logout/', views.admin_logout, name = "admin_logout"),
	url(r'^taxi_xls_upload/$', views.taxi_csv_upload, name='taxi_csv_upload'),
        url(r'^bulk_image_upload/$', views.bulk_image_upload, name='bulk_image_upload'),
#	url(r'^taxi/(?P<pk>[\w\-]+)/$', views.taxi_detail, name='taxi_detail'),
        url(r'^taxi/(?P<pk>[\w|\W]+)/$', views.taxi_detail, name='taxi_detail'),
        url(r'^complaint/', views.complaint_form, name='complaint_form'),
        url(r'^complaint_success/(?P<pk>[\w\-]+)/$', views.complaint_success, name='complaint_success'),
#        url(r'^complaint_list/$', views.complaint_list, name='complaint_list'),
        url(r'^complaint_resolve/$', views.complaint_resolve, name='complaint_resolve'),
        url(r'^complaint_view/(?P<pk>[\w\-]+)/$', views.complaint_view, name='complaint_view'),
        url(r'^taxi_list/$', views.taxi_list, name='taxi_list'),
        url(r'^taxi_emergency/$', views.taxi_emergency, name='taxi_emergency'),
        url(r'^health_check/$', views.health_check, name='health_check'),
        url(r'^admin/logout/$', views.admin_logout),
        url(r'^admin_password_change/$',views.admin_password_change,name="admin_password_change"),
        url(r'^admin_password_change_done/$',views.admin_password_change_done,name="admin_password_change_done"),
        url(r'^admin_forgot_password/$',views.admin_forgot_password,name="admin_forgot_password"),
        url(r'^enter_otp/$',views.enter_otp,name="enter_otp"),
        url(r'^reset_admin_password/$',views.reset_admin_password,name="reset_admin_password"),
        url(r'^api/v1/get_driver_owner_details/$',views.TaxiDriverOwner.as_view()),
        url(r'^api/v1/get_complaints/$',views.TaxiComplaints.as_view()),
        url(r'^docs/$', swagger.schema_view, name="schema_view"),
        url(r'^ratings/$',views.Ratings,name='Ratings'),
        url(r'^customer_rating/$',views.customer_rating,name='Ratings'),
        url(r'^owner_images_migration/$',views.OwnerImagesMigration,name='owner_images_migration'),
        url(r'^driver_images_migration/$',views.DriverImagesMigration,name='driver_images_migration'),
        url(r'^vehicle_qrcode_migration/$',views.VehicleQrCodeMigration,name='vehicle_qrcode_migration'),
        url(r'^driver_qrcode_migration/$',views.DriverQrCodeMigration,name='driver_qrcode_migration'),

]       

handler404 = views.handler404

