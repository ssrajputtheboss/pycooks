from geopy.distance import geodesic
from geopy.distance import great_circle
from geopy.geocoders import Nominatim


class DistanceFinder():
    def __init__(self):
        self.geolocator = Nominatim(user_agent="p_finder")
    def getdistance(self,city1,city2):
        l1 = self.geolocator.geocode(city1)
        l2 = self.geolocator.geocode(city2)
        start_point=(float(l1.longitude),float(l1.latitude))
        end_point=(float(l2.longitude),float(l2.latitude))
        d=round(geodesic(start_point,end_point).kilometers,2)
        #d2=round(great_circle(start_point,end_point).kilometers,2)
        return d

city1=input('city1: ')
city2=input('city2 :')
try:
    d=DistanceFinder()
    print(d.getdistance(city1,city2),'kilometers')
except:
    print('An Error occured')
