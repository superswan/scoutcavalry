import json
import ssl
from urllib.request import urlopen
from urllib.request import Request

from bcolors import bcolors

ip = None
def getGeoLoc(ip):
    if ip == None:
        ip = urlopen('http://icanhazip.com')
        ip = ip.read().decode("utf-8")

    url = f'https://api.ipgeolocationapi.com/geolocate/{ip}'

    req = Request(
        url,
        data=None,
        headers={
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' 
        }
    )

    print(f"{bcolors.OKBLUE}[*] Getting geolocation data for {ip}{bcolors.ENDC}")
    response = urlopen(req)
    data = response.read().decode("utf-8")
    data = json.loads(data)
    continent = str(data["continent"])
    country_name = str(data["ioc"])
    city_name = "Disabled"
    latitude = str(data["geo"]["latitude"])
    longitude = str(data["geo"]["longitude"])
    
    return (continent, country_name, city_name, latitude, longitude)
    
