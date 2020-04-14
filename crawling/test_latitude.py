
from urllib.request import urlopen
import json

location = "서울시 마포구 토정로 11길 47-1"
data = urlopen("http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address=" + location)
json = json.loads(data.read())

latitude = json["results"][0]["geometry"]["location"]["lat"]
longitude = json["results"][0]["geometry"]["location"]["lng"]

print(latitude)
print(longitude)
