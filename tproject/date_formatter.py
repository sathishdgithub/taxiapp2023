def date_form(date):
    t = str(date).strip().split('/')
    if len(t) == 3:
       d,m,y = t
       if (len(y)==4) and (int(m)<=12 and int(m)>=1): 
           return y+'-'+m+'-'+d
       elif (len(y)==4) and (int(d)<=12 and int(d)>=1):
           return y+'-'+d+'-'+m
    return None



"""
KeyboardInterrupt
>>> for index,row in data1.iterrows():
...     c = City_Code.objects.get(city_code='TPT')
...     p = Taxi_Detail(number_plate=row["AUTONUMBER"],traffic_number=row["TRAFFICNUMBER"],driver_name=row["NAME"],son_of=row["FATHERNAME"],date_of_birth=date_form(row["DATE OF BIRTH"]),phone_number=row["PHONENUMBER"],address=row["ADDRESS"],aadhar_number=row["AADHARNUMBER"],driving_license_number=row["DRIVINGLICENCENUMBER"],date_of_validity=date_form(row["DATE OF VALIDITY"]),autostand=row['AUTOSTAND'],union=row['UNION'],insurance=date_form(row["INSURANCE"]),capacity_of_passengers=row["CAPACITY OF PASSANGER"],pollution=date_form(row["POLLUTION"]),engine_number=row["ENGINE NUMBER"],chasis_number=row["CHASISNUMBER"],owner_driver=row["OWNERDRIVER"],city=c)
...     if len(row["TRAFFICNUMBER"]) > 3:
...         p.save()
... 
>>> data2 = pd.read_csv('tpt_new.csv')
>>> for index,row in data2.iterrows():
...     c = City_Code.objects.get(city_code='TPT')
...     p = Taxi_Detail(number_plate=row["AUTONUMBER"],traffic_number=row["TRAFFICNUMBER"],driver_name=row["NAME"],son_of=row["FATHERNAME"],date_of_birth=date_form(row["DATE OF BIRTH"]),phone_number=row["PHONENUMBER"],address=row["ADDRESS"],aadhar_number=row["AADHARNUMBER"],driving_license_number=row["DRIVINGLICENCENUMBER"],date_of_validity=date_form(row["DATE OF VALIDITY"]),autostand=row['AUTOSTAND'],union=row['UNION'],insurance=date_form(row["INSURANCE"]),capacity_of_passengers=row["CAPACITY OF PASSANGER"],pollution=date_form(row["POLLUTION"]),engine_number=row["ENGINE NUMBER"],chasis_number=row["CHASISNUMBER"],owner_driver=row["OWNERDRIVER"],city=c)
...     if len(row["TRAFFICNUMBER"]) > 3:
...         p.save()
... 
"""
