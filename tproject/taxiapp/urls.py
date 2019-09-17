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
        # url(r'^vehicle_qrcode_migration/$',views.VehicleQrCodeMigration,name='vehicle_qrcode_migration'),
        # url(r'^driver_qrcode_migration/$',views.DriverQrCodeMigration,name='driver_qrcode_migration'),
        #url(r'^image_grands_public/$',views.ImageGrandPublic,name='image_grands_public'),
        url(r'^driver_image_validation/$',views.DriverImageValidation,name='driver_image_validation'),
        url(r'^owner_image_validation/$',views.OwnerImageValidation,name='owner_image_validation'),
        url(r'^terms_of_use/',views.Terms_Of_Use,name='Terms_Of_Use'),
        url(r'^privacy_policy/',views.Privacy_Policy,name='Privacy_Policy'),
        url(r'^about_us/',views.About_Us,name='About_Us'),
        url(r'^vehice_registrations/',views.Vehice_Registration,name='Vehice_Registration'),
        url(r'^vehicle_register_details/',views.Vehicle_Register_Details,name='Vehicle_Register_Details'),
        url(r'^add_vehicle/',views.Add_Vehicle,name='Add_Vehicle'),
        url(r'^register_vehicle/',views.Register_Vehicle,name='Register_Vehicle'),
        url(r'^delete_vehicle/',views.Delete_Vehicle,name='Delete_Vehicle'),
        url(r'^delete_complaint/',views.Delete_Complaint,name='Delete_Complaint'),
        url(r'^delete_rating/',views.Delete_Rating,name='Delete_Rating'),
        url(r'^add_driver/',views.Add_Driver,name='Add_Driver'),
        url(r'^add_vehicle_details',views.Add_Vehicle_Details,name='Add_Vehicle_Details'),
        url(r'^add_driver_details',views.Add_Driver_Details,name='Add_Driver_Details'),
        #remove later
        #url(r'^SendSMS_Owner_Driver',views.SendSMS_Owner_Driver,name='SendSMS_Owner_Driver'),
        url(r'delete_driver',views.Delete_Driver,name='Delete_Driver'),
        url(r'disassociate_driver',views.Disassociate_Driver,name='Disassociate_Driver'),
        url(r'^edit_driver/',views.Edit_Driver,name='Edit_Driver'),
        url(r'associate_driver',views.Associate_Driver,name='Associate_Driver'),
        url(r'associate_vehicletodriver',views.Associate_VehicleToDriver,name='Associate_VehicleToDriver'),
        url(r'populate_numberplate',views.Populate_Numberplate,name='Populate_Numberplate'),
        url(r'populate_trafficnumber',views.Populate_TrafficNumber,name='Populate_TrafficNumber'),
        # url(r'allocationlist_driver',views.Allocationlist_Driver,name='Allocationlist_Driver'),
        url(r'^dashboard/',views.Dashboard,name='Dashboard'),
        url(r'^vehicle_list/',views.Vehicles_List,name='Vehicles_List'),
        url(r'^driver_list/',views.Driver_List,name='Driver_List'),
        url(r'^complaints_list/',views.Complaints_List,name='Complaints_List'),
        url(r'^customer_rating_list/',views.Customer_Rating_List,name='Customer_Rating_List'),
        url(r'^vehicle_registration_list/',views.Vehicle_Registration_List,name='Vehicle_Registration_List'), 
        url(r'^vehicle_export_To_csv/',views.Vehicle_Export_To_Csv,name='Vehicle_Export_To_Csv'),
        url(r'^drivers_export_To_csv/',views.Drivers_Export_To_Csv,name='Drivers_Export_To_Csv'),
        url(r'^upload_images/',views.Upload_Images,name='Upload_Images'),
        url(r'^delete_vehicle_registration/',views.Delete_Vehicle_Registration,name='Delete_Vehicle_Registration'),
        url(r'^driver/(?P<pk>[\w|\W]+)/$', views.Driver_Detail, name='Driver_Detail'),
]       

handler404 = views.handler404

