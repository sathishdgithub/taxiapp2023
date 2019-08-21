from rest_framework import serializers
from models import Taxi_Detail
from models import Complaint_Statement
from models import Driver
from models import Active
from models import Owner
from models import Vehicle
from models import City_Code
from models import Vehicle_type



class CityCodeSerialize(serializers.ModelSerializer):
    class Meta:
        model = City_Code
        fields = ('city','city_code')

class DriverSerialize(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('driver_name','address','date_of_birth','son_of','phone_number','aadhar_number',
        'driver_image', 'dl_expiry','dl_number', 'blood_group')

class OwnerSerialize(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('owner_name','address','date_of_birth','son_of','phone_number','aadhar_number',
        'owner_image', 'dl_expiry','dl_number', 'blood_group')

class TaxiDriverOwnerSerialize(serializers.ModelSerializer):
    vehicle_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field='vehicle_type'
    )
    city = CityCodeSerialize(many=False)
    owner = OwnerSerialize(many=False)
    drivers = DriverSerialize(many=True)
    class Meta:
        model =Vehicle
        fields = ('traffic_number','number_plate','autostand','union','insurance',
                   'pollution','engine_number','chasis_number','num_of_complaints','qr_code',
                    'vehicle_make','vehicle_model','mfg_date','insurance_provider','insurance_number','capacity_of_passengers',
                    'rc_expiry','vehicle_type','city','owner','drivers')


class TaxiComplaintsSerialize(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field='city'
    )    
    assigned_to = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    taxi = serializers.SlugRelatedField(
        read_only=True,
        slug_field='driver_name'
    )
    reason = serializers.SlugRelatedField(
        read_only=True,
        slug_field='reason'
    )
    
    class Meta:
        model = Complaint_Statement
        fields = ('complaint_number', 'taxi','reason','area','city','origin_area',
        'destination_area','phone_number','complaint','assigned_to','resolved')
