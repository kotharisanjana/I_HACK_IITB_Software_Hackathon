from django.shortcuts import render,redirect
import requests
from django.http import HttpResponseRedirect
import json
import random
import sys
import math
import gmplot
import folium
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import geojson
from django.http import JsonResponse

latitude = 19.99
longitude = 73.78
apiKey= 'DpKgJ3b66FDQhW1dbcHsZo-nfo4tdaumLmYvnw55XmU'
charging_stations=[[40.7054,-74.0081],[40.7030,-74.0102],[40.7068, -74.0168],[40.7086,-74.0114],[40.7123,-74.0099]]

destination = {"latitude" : 40.704240, "longitude" : -74.009400}


uber_data = [
	{
		"uber_id": 1,
		"latitude": 40.706083,
		"longitude": -74.011125
	},
	{
		"uber_id": 2,
		"latitude": 40.705400,
		"longitude": -74.009750
	},
	{
		"uber_id": 3,
		"latitude": 40.703708,
		"longitude": -74.013015
	},
	{
		"uber_id": 4,
		"latitude": 40.709467,
		"longitude": -74.013702
	},
	{
		"uber_id": 5,
		"latitude": 40.712102,
		"longitude": -74.009235
	},
	{
		"uber_id": 6,
		"latitude": 40.709037,
		"longitude": -74.003186
	},
	{
		"uber_id": 7,
		"latitude": 40.705686,
		"longitude": -74.004603
	}
]



def generate_random_loc(lat, lon):
    hex1 = '%012x' % random.randrange(16**12) # 12 char random string
    flt = float(random.randint(0,100))
    dec_lat = random.random()/100
    dec_lon = random.random()/100
    return lon+dec_lon, lat+dec_lat

def clean_iso_coords(coord_list,listtype):
    lon=[]
    lat=[]
    coor_lat_lon=[]
    coor_lon_lat=[]
    i=0
    if listtype=="iso":
        for entry in coord_list:
            temp=entry.replace('"','')
            a,b= temp.split(',',1)
            lat.append(float(a))
            lon.append(float(b))
            coor_lat_lon.append((float(a),float(b)))
            coor_lon_lat.append((float(b),float(a)))
            i+=1
        return lat,lon,coor_lat_lon, coor_lon_lat
    

def plot_route(data):
    lat=[]
    lon=[]
    labs=[]
    coords=[]
    n=len(data['response']['route'][0]['leg'][0]['maneuver'])
    for i in range(n):
        a=data['response']['route'][0]['leg'][0]['maneuver'][i]['position']['latitude']
        b=data['response']['route'][0]['leg'][0]['maneuver'][i]['position']['longitude']
        labs.append(i)
        lat.append(float(a))
        lon.append(float(b))
        coords.append((float(a),float(b)))

    my_map=old_map
    folium.Marker([lat[0], lon[0]],popup = 'A').add_to(my_map)
    folium.Marker([lat[n-1], lon[n-1]],popup = 'B').add_to(my_map)
    folium.PolyLine(locations = coords, line_opacity = 0.5).add_to(my_map)
    my_map.save("C:\\Users\\Saanika\\Desktop\\map3.html") 

    

            
def plot_isolinemap(coord_list1, coord_list2,coords,data):
    
    m = folium.Map(coords[0], zoom_start=6, tiles='cartodbpositron')
    polygon = Polygon(coords)
    folium.GeoJson(polygon).add_to(m)
    folium.LatLngPopup().add_to(m)
    lat=[]
    lon=[]
    labs=[]
    coords_route=[]
    n=len(data['response']['route'][0]['leg'][0]['maneuver'])
    for i in range(n):
        a=data['response']['route'][0]['leg'][0]['maneuver'][i]['position']['latitude']
        b=data['response']['route'][0]['leg'][0]['maneuver'][i]['position']['longitude']
        labs.append(i)
        lat.append(float(a))
        lon.append(float(b))
        coords_route.append((float(a),float(b)))

    for entry in charging_stations:
        folium.Marker(entry,popup='Charging Port',icon=folium.Icon(color='red')).add_to(m)
    
    for uber in uber_data:
        folium.Marker([uber['latitude'],uber['longitude']],popup=uber['uber_id'],icon=folium.Icon(color='green')).add_to(m)

    folium.Marker([lat[0], lon[0]],popup = 'A').add_to(m)
    folium.Marker([lat[n-1], lon[n-1]],popup = 'B').add_to(m)
    folium.PolyLine(locations = coords_route, line_opacity = 0.5).add_to(m)
    m.save("C:\\Users\\Saanika\\Desktop\\map3.html")
    
    return m

def in_isoline(coor,a,b):
    new_coor=[]
    for entry in coor:
        a= float(entry[0])
        b=float(entry[1])
        new_coor.append([float(a),float(b)])
    polygon = Polygon(new_coor) # create polygon
    point = Point(a,b)
    print(polygon.contains(point))
    print(polygon)
    print(polygon.bounds)
    return polygon.contains(point)


def nocharge(request):
    '''if request.method == 'POST':
        car_number = request.POST['car_number']'''
    return render(request,'helpcall.html',{})



##on helppage
def sendloc(request):
    l1,l2=generate_random_loc(latitude,longitude)
    print(l1,l2)
    
    l1=40.699352
    l2=-74.012000

    la1= 40.7134
    la2=-74.0077

    latitude_a = l1
    longitude_a = l2

    min_time_1 = sys.maxsize
    min_time_2 = sys.maxsize
    min_time_3 = sys.maxsize
    for ubers in uber_data:
        lat, lon = ubers['latitude'], ubers['longitude']
        response = requests.get('https://wse.ls.hereapi.com/2/findsequence.json?start=Charged-Uber;'+str(lat)+','+str(lon)+'&destination1=Discharged-Uber;'+str(latitude_a)+','+str(longitude_a)+'&end=Destination;'+str(destination["latitude"])+','+str(destination["longitude"])+'&mode=fastest;car&apiKey=YJLC8FU3mLEGG7CjZ8Pyq-CwPoJqw6EvAXbYrFUdZuQ')
        answer = response.json()
        if(int(answer['results'][0]['time']) < min_time_1):
            min_time_1 = int(answer['results'][0]['time'])
            uber_lat_1, uber_lon_1 = lat, lon
    charge_consumed = mileage * dist_travelled
    time_left = c * (total_charge - charge_consumed)
    for stations in charging_data:
        lat, lon = stations['latitude'], stations['longitude']
        res = requests.get('https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey=YJLC8FU3mLEGG7CjZ8Pyq-CwPoJqw6EvAXbYrFUdZuQ&waypoint0=geo!'+str(latitude_a)+','+str(longitude_a)+'&waypoint1=geo!'+str(lat)+','+str(lon)+'&mode=fastest;car;traffic:enabled')
        answer = res.json()
        for i in answer['response']['route']:
            x = i['summary']['tavelTime']
            if(int(x) < min_time_2):
                min_time_2 = int(x)
                station_lat, station_lon = lat, lon
                
    for ubers in uber_data:
        lat, lon = ubers['latitude'], ubers['longitude']
        response = requests.get('https://wse.ls.hereapi.com/2/findsequence.json?start=Charged-Uber;'+str(lat)+','+str(lon)+'&destination1=Discharged-Uber;'+str(station_lat)+','+str(station_lon)+'&end=Destination;'+str(destination["latitude"])+','+str(destination["longitude"])+'&mode=fastest;car&apiKey=YJLC8FU3mLEGG7CjZ8Pyq-CwPoJqw6EvAXbYrFUdZuQ')
        answer = response.json()
        if(int(answer['results'][0]['time']) < min_time_3):
            min_time_3 = int(answer['results'][0]['time'])
            uber_lat_2, uber_lon_2 = lat, lon
            
            
    if(min_time_1 < min_time_3):
        path = {'charged_lat' : uber_lat, 'charged_lon' : uber_lon, 'discharged_lat' : latitude_a, 'discharged_lon' : longitude_a, 'desination_lat':destination['latitude'], 'destination_lon' : destination['longitude']}
    elif(time_left < min_time_2 & min_time_1 > min_time_3):
        path ={'charged_lat' : uber_lat_2, 'charged_lon' : uber_lon_2, 'discharged_lat' : station_lat, 'discharged_lon' : station_lon, 'desination_lat':destination['latitude'], 'destination_lon' : destination['longitude']}
    
    
    
    temp= requests.get('https://isoline.route.ls.hereapi.com/routing/7.2/calculateisoline.json?apiKey='+apiKey+'&mode=shortest;car;traffic:disabled&start=geo!'+str(l1)+','+str(l2)+'&range=1000&rangetype=distance')
    isoresponse=temp.json()
    dims=isoresponse['response']['isoline'][0]['component'][0]['shape']
    print(len(dims))
    dims1,dims2,coord_la_lo,coord_lo_la=clean_iso_coords(dims,"iso")
    print(in_isoline(coord_la_lo,l1,l2))
    
    
    response = requests.get('https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey='+str(apiKey)+'&waypoint0=geo!'+str(l1)+','+str(l2)+'&waypoint1=geo!'+str(la1)+','+str(la2)+'&departure=now&mode=fastest;publicTransport&combineChange=true')
    geodata = response.json()
    turns=len(geodata['response']['route'][0]['leg'][0]['maneuver'])
    plot_isolinemap(dims1, dims2,coord_lo_la,geodata)


    wresponse = requests.get('https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey='+str(apiKey)+'&product=observation&name=New-York')
    answer = wresponse.json()

    visit = []
    not_visit = []
    a = answer['observations']['location']
    for i in a:
        l = i['observation']
        daylight = l[0]['daylight']
        sky = l[0]['skyDescription']
        visibility = l[0]['visibility']
        elevation = l[0]['elevation']
        city = l[0]['city']
        if daylight == 'D':
            if sky == 'Overcast':
                if float(visibility) < 14:
                    not_visit.append(city)
                else:
                    visit.append(city)
        else:
            if float(visibility) < 14:
                not_visit.append(city)
            else:
                visit.append(city)
        if city in visit:
            if float(elevation) > 5.0:
                if city not in not_visit:
                    not_visit.append(city)
            visit.remove(city)
    send = {}
    i = 0
    for cities in not_visit:
        send[i] = cities
        i += 1
    return render(request,"trial_routes.html",{'cities':send.values()})        



def busroutes(request):
    print("A")
    response = requests.get('https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey=DpKgJ3b66FDQhW1dbcHsZo-nfo4tdaumLmYvnw55XmU&waypoint0=geo!52.530,13.326&waypoint1=geo!52.513,13.407&departure=now&mode=fastest;publicTransport&combineChange=true')
    geodata = response.json()
    print(type(geodata.keys))
    return render(request, 'trial_routes.html', {'data':geodata})
