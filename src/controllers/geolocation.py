import requests
from geopy.geocoders import Nominatim

# Get location data from ipinfo.io
response = requests.get('https://ipinfo.io')
data = response.json()

# Extract latitude and longitude
location = data['loc'].split(',')
latitude = location[0]
longitude = location[1]

# latitude = 23.2548535
# longitude = 77.4000001

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="GetLoc")

# Get address using geopy
location = geolocator.reverse(f"{latitude}, {longitude}")

# Print the address
print("Address:", location.address)

# Print latitude and longitude
print("Latitude:", latitude)
print("Longitude:", longitude)