from django.contrib import admin
from django.contrib.auth.models import User

from .models import *
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sites.models import Site
from taxiapp.models import MyUser,Vehicle,Driver,Owner,Active,Vehicle_type,Rating_Type,Rating_Reason,Customer_Rating
from django.core.urlresolvers import reverse
from imagekit.admin import AdminThumbnail


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email','sms_number','whatsapp_number','city','area','location', 'is_admin', 'is_staff')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_number = user.city.city_code+'-ID-'+str(self.instance.city.police_no+1).zfill(4)
        t = City_Code.objects.get(id=self.instance.city.id)
        t.taxi_no = t.police_no+1
        t.save()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'sms_number', 'whatsapp_number', 'area','city','location','is_active', 'is_admin','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'sms_number', 'whatsapp_number','area','city','is_admin','is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('sms_number','whatsapp_number', 'area','city','location')}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'sms_number','city','area','location','password1', 'password2','is_admin','is_staff',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class TaxiAdminCreationForm(forms.ModelForm):
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate','traffic_number','driver_name','address','city','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver','driver_image','driver_image_name')
    def save(self, *args, **kwargs):
        if self.instance.traffic_number.strip()=='' or self.instance.traffic_number.strip()=='-':
            self.instance.traffic_number = self.instance.city.city_code+'-TR-'+str(self.instance.city.taxi_no+1).zfill(5)
        t = City_Code.objects.get(id=self.instance.city.id)
        t.taxi_no = t.taxi_no+1
        t.save()
        return super(TaxiAdminCreationForm, self).save(*args, **kwargs)


class TaxiAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate','traffic_number','driver_name','address','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver','driver_image','driver_image_name')

class TaxiAdmin(admin.ModelAdmin):
    #def has_delete_permission(request):
    #    return request.user.is_staff and request.user.is_admin

    exclude = ('qr_code','num_of_complaints')
    form = TaxiAdminCreationForm
    change_form = TaxiAdminUpdateForm
    list_display = ('number_plate_', 'traffic_number','name','phone_number','owner_driver','profile_pic','qr_image',)
    search_fields = ('number_plate', 'traffic_number','driver_name','phone_number', )
    def qr_image(self, obj):  # receives the instance as an argument
        return '<img width=75 height=75 src="{thumb}" />'.format(
            thumb=obj.qr_code.url,
        )
    qr_image.allow_tags = True
    qr_image.short_description = 'QR Code'
    

 #   profile_pic = AdminThumbnail(image_field='driver_image')
  #  profile_pic.short_description = 'Driver Picture'
    
    def profile_pic(self, obj):  # receives the instance as an argument
        url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.model_name),  args=[obj.id] )
        return '<img width=75 height=75 src="{thumb}" />'.format(
            thumb=obj.driver_image_thumbnail.url,
        )
    profile_pic.allow_tags = True
    profile_pic.short_description = 'Driver Picture'
    def name(self,obj):
        return str(obj.driver_name)
    name.allow_tags = True
    name.short_description = "NAME"

    def number_plate_(self, obj):  # receives the instance as an argument
        np = obj.get_number_plate.replace('-','')
        try:
            k = np[0]
            for i in range(1,len(np)):
                if np[i]=='-':
                    pass
                elif ((np[i-1].isalpha()) and (np[i].isdigit())) or ((np[i-1].isdigit()) and (np[i].isalpha())):
                    k = k + ' '+np[i]
                else:
                    k = k + np[i]
            return k
        except Exception as e:
            return obj.get_number_plate
    number_plate_.allow_tags = True
    number_plate_.short_description = 'Number Plate'

    def owner_driver(self,obj):
        return str(obj.owner_driver)
    owner_driver.allow_tags = True
    owner_driver.short_description = "Owner/Driver"
    def get_form(self, request, obj=None, **kwargs):
       if obj is not None:
          kwargs['form'] = self.change_form
       return super(TaxiAdmin, self).get_form(request, obj, **kwargs)


class ComplaintStatementAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin
    list_display = ('complaint_id', 'number_plate', 'owner_name', 'phone_number', 'reason','resolved','allocated_to')
    def complaint_id(self, obj):
        return str(obj.complaint_number)
    complaint_id.short_description = 'Complaint ID'
    def number_plate(self, obj):
        if (obj.vehicle is not None) :
            return obj.vehicle.traffic_number
    number_plate.short_description = 'Number Plate'
    def owner_name(self, obj):
        if (obj.vehicle is not None and obj.vehicle.owner is not None) :
            return obj.vehicle.owner.owner_name
    owner_name.short_description = 'Owner Name'
    def reason(self, obj):
        return obj.reason
    reason.short_description = 'Reason'
    def allocated_to(self, obj):
        if not obj.assigned_to:
            return "Not Assigned"
        return str(obj.assigned_to.id)+' | '+str(obj.assigned_to.sms_number)
    allocated_to.short_description = 'Allocated To'
    def phone_number(self,obj):
        return str(obj.phone_number)
    phone_number.short_description = "Phone Number"


class CityCodeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('police_no','taxi_no','complaint_no')
    list_display = ('city','city_code','whatsapp','sms','distress')

class ReasonsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    list_display = ('reason_id','reason')
    def reason_id(self,obj):
        return 'CR-'+str(obj.id).zfill(3)

class VehicleAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('qr_code','created_time','modified_by','modified_time')
    list_display = ('traffic_number','number_plate','vehicle_type','is_owner_driver','qr_image')
    def qr_image(self, obj):  # receives the instance as an argument
        return '<img width=75 height=75 src="{thumb}" />'.format(
            thumb=obj.qr_code.url,
        )
    qr_image.allow_tags = True
    qr_image.short_description = 'QR Code'

class DriverAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('qr_code','created_time','modified_by','modified_time','qr_image','is_image_verified')
    list_display = ('traffic_number','driver_name','phone_number','dl_number','driver_image_name')
    # def qr_image(self, obj):  # receives the instance as an argument
    #     return '<img width=75 height=75 src="{thumb}" />'.format(
    #         thumb=obj.qr_code.url,
    #     )
    # qr_image.allow_tags = True
    # qr_image.short_description = 'QR Code'

class OwnerAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('created_time','modified_by','modified_time','is_image_verified')
    list_display = ('owner_name','date_of_birth','phone_number','owner_image','dl_number')

class RatingTypeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('created_time','modified_by','modified_time')
    list_display = ('rating_type','active')
    def active(self, obj):
        return str(obj.active)
    active.short_description = 'Active'

class RatingReasonAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('created_time','modified_by','modified_time')
    list_display = ('rating_type','reason','active')
    def rating_type(self, obj):
        return str(obj.rating_type)
    rating_type.short_description = 'Rating Type'
    def active(self, obj):
        return str(obj.active)
    active.short_description = 'Active'

class CustomerRatingAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff and request.user.is_admin    
    exclude = ('created_time','modified_by','modified_time')
    list_display = ('vehicle','driver','reason','phone_number','destination_area','origin_area')
    def vehicle(self, obj):
        return str(obj.vehicle)
    vehicle.short_description = 'Vehicle Number'
    def driver(self, obj):
        return str(obj.driver)
    driver.short_description = 'Driver'

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(City_Code,CityCodeAdmin)
admin.site.register(Reasons,ReasonsAdmin)
admin.site.register(Taxi_Detail,TaxiAdmin)
admin.site.register(Vehicle,VehicleAdmin)
admin.site.register(Driver,DriverAdmin)
admin.site.register(Owner,OwnerAdmin)
admin.site.register(Active)
admin.site.register(Vehicle_type)
admin.site.register(Rating_Type,RatingTypeAdmin)
admin.site.register(Rating_Reason,RatingReasonAdmin)
admin.site.register(Customer_Rating,CustomerRatingAdmin)
admin.site.register(Complaint_Statement,ComplaintStatementAdmin)
admin.site.unregister(Site)
admin.site.site_header = 'SafeAutoTaxi Administration'
#admin.site.register(Admin_Detail)
#admin.site.register(User_Complaint)
admin.site.register(Source)