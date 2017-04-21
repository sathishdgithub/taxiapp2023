from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sites.models import Site
from taxiapp.models import MyUser

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email','sms_number','whatsapp_number','area','city','location')

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
        fields = ('email', 'password', 'sms_number', 'whatsapp_number', 'area','city','location','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'sms_number', 'whatsapp_number', 'area','city','location','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('sms_number','whatsapp_number', 'area','city','location')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'sms_number','area','city','location','password1', 'password2',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class TaxiAdminCreationForm(forms.ModelForm):
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate','driver_name','address','city','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver','driver_image')
    def save(self, *args, **kwargs):
        self.instance.traffic_number = self.instance.city.city_code+'-TR-'+str(self.instance.city.taxi_no+1).zfill(5)
        t = City_Code.objects.get(id=self.instance.city.id)
        t.taxi_no = t.taxi_no+1
        t.save()
        return super(TaxiAdminCreationForm, self).save(*args, **kwargs)


class TaxiAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate','driver_name','address','date_of_birth','son_of','phone_number', 'aadhar_number','driving_license_number','date_of_validity','autostand','union','insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver','driver_image')

class TaxiAdmin(admin.ModelAdmin):
    exclude = ('qr_code','num_of_complaints','traffic_number')
    form = TaxiAdminCreationForm
    change_form = TaxiAdminUpdateForm
    list_display = ('number_plate', 'traffic_number','driver_name','num_of_complaints','owner_driver','profile_pic','qr_image')
    def qr_image(self, obj):  # receives the instance as an argument
        return '<img width=75 height=75 src="{thumb}" />'.format(
            thumb=obj.qr_code.url,
        )
    qr_image.allow_tags = True
    qr_image.short_description = 'QR Code'
    def profile_pic(self, obj):  # receives the instance as an argument
        return '<img width=75 height=75 src="{thumb}" />'.format(
            thumb=obj.driver_image.url,
        )
    profile_pic.allow_tags = True
    profile_pic.short_description = 'Driver Picture'
    def get_form(self, request, obj=None, **kwargs):
       if obj is not None:
          kwargs['form'] = self.change_form
       return super(TaxiAdmin, self).get_form(request, obj, **kwargs)


class ComplaintStatementAdmin(admin.ModelAdmin):
    list_display = ('complaint_id', 'number_plate', 'driver_name', 'phone_number', 'reason','resolved','allocated_to')
    def complaint_id(self, obj):
        return str(obj.complaint_number)
    complaint_id.short_description = 'Complaint ID'
    def number_plate(self, obj):
        return obj.taxi.traffic_number
    number_plate.short_description = 'Number Plate'
    def driver_name(self, obj):
        return obj.taxi.driver_name
    driver_name.short_description = 'Driver Name'
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
    exclude = ('police_no','taxi_no','complaint_no')
    list_display = ('city','city_code','whatsapp','sms','distress')

class ReasonsAdmin(admin.ModelAdmin):
    list_display = ('reason_id','reason')
    def reason_id(self,obj):
        return 'CR-'+str(obj.id).zfill(3)

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(City_Code,CityCodeAdmin)
admin.site.register(Reasons,ReasonsAdmin)
admin.site.register(Taxi_Detail,TaxiAdmin)
admin.site.register(Complaint_Statement,ComplaintStatementAdmin)
admin.site.unregister(Site)

#admin.site.register(Admin_Detail)
#admin.site.register(User_Complaint)
