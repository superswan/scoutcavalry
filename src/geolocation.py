from urllib.request import urlopen 
import json
from bcolors import bcolors

ip = None
def getGeoLoc(ip):
    if ip == None:
        ip = urlopen('http://icanhazip.com')
        ip = ip.read().decode("utf-8")

    url = f'https://ipvigilante.com/{ip}'
    print(f"{bcolors.OKBLUE}[*] Getting geolocation data for {ip}{bcolors.ENDC}")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    data = json.loads(data)
    continent = str(data["data"]["continent_name"])
    country_name = str(data["data"]["country_name"])
    city_name = str(data["data"]["city_name"])
    latitude = str(data["data"]["latitude"])
    longitude = str(data["data"]["longitude"])
    
    return (continent, country_name, city_name, latitude, longitude)
    
