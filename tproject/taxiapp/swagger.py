from rest_framework.decorators import renderer_classes,api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response
#from rest_framework.views import APIView
# noinspection PyArgumentList
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    #print("---inside schema view-----")
    # noinspection PyArgumentList
    schema = coreapi.Document(
    title='Taxi App',
    #url='https://www.safeautotaxi.com/',
    url='',
    content={        
        'taxidetails': coreapi.Link(
            url='/api/v1/get_driver_owner_details',
            action='get',
            fields=[
                coreapi.Field(
                    name='cityCode',
                    required=False,
                    location='query',
                    description='Enter City Code.'
                ),
                coreapi.Field(
                    name='rangeFrom',
                    required=False,
                    location='query',
                    description='Traffic Number starts from.'
                ),
                coreapi.Field(
                    name='rangeTo',
                    required=False,
                    location='query',
                    description='Traffic Number Ends to.'
                ),
                coreapi.Field(
                    name='taxiIds',
                    required=False,
                    location='query',
                    description='Traffic Numbers.'
                ),
                coreapi.Field(
                    name='numberPlates',
                    required=False,
                    location='query',
                    description='Number Plates.'
                ),
                coreapi.Field(
                    name='page',
                    required=False,
                    location='query',
                    description='Page Number.'
                ),
                coreapi.Field(
                    name='limit',
                    required=False,
                    location='query',
                    description='No Of Records per page.'
                )
            ],
            #description='Return Taxi Details as per CityCode and Traffic Number Range.'
            description='',
        ),
        'taxiComplaints': coreapi.Link(
            url='/api/v1/get_complaints',
            action='get',
            fields=[
                coreapi.Field(
                    name='cityCode',
                    required=False,
                    location='query',
                    description='Enter City Code.'
                ),
                coreapi.Field(
                    name='rangeFrom',
                    required=False,
                    location='query',
                    description='Traffic Number starts from.'
                ),
                coreapi.Field(
                    name='rangeTo',
                    required=False,
                    location='query',
                    description='Traffic Number Ends to.'
                ),
                coreapi.Field(
                    name='taxiIds',
                    required=False,
                    location='query',
                    description='Traffic Numbers.'
                ),
                coreapi.Field(
                    name='numberPlates',
                    required=False,
                    location='query',
                    description='Number Plates.'
                ),
                coreapi.Field(
                    name='page',
                    required=False,
                    location='query',
                    description='Page Number.'
                ),
                coreapi.Field(
                    name='limit',
                    required=False,
                    location='query',
                    description='No Of Records per page.'
                )
            ],
            #description='Return Taxi Details as per CityCode and Traffic Number Range.'
            description=''
        )
    }
)
    # schema = generator.get_schema(request)
    return response.Response(schema)