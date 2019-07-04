from rest_framework import serializers
from models import Taxi_Detail
from models import Complaint_Statement


class TaxiDriverOwnerSerialize(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field='city'
     )
    class Meta:
        model = Taxi_Detail
        fields = ('number_plate', 'traffic_number','driver_name','son_of','date_of_birth','phone_number',
        'address','city','aadhar_number','driving_license_number','date_of_validity','autostand','union',
        'insurance','capacity_of_passengers','pollution','engine_number','chasis_number','owner_driver',
        'num_of_complaints','driver_image','qr_code','driver_image_name')

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
