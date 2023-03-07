from api import api_key
import requests
import pyperclip
import pandas as pd
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
# auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# OWM_Endpoint = 'http://api.openweathermap.org/data/2.5/forecast'
# OWM_Endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
OWM_Endpoint = 'https://api.openweathermap.org/data/3.0/onecall'

parameters = {
    'lat': 39.739235,
    'lon': -104.990250,
    # 'id': 524901,
    'appid': api_key,
    'exclude': 'current,minutely,daily'
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()

data = response.json()
# pyperclip.copy(data)
hourly = pd.DataFrame(data['hourly'])

# a[start:stop] # itmes start through stop-1
# a[start:] # items start through the rest of the array
# a[:stop] # items from the beginning through stop-1
# a[:] # copy of the whole array

weather_slice = data['hourly'][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    print('bring umbrella')
    message = client.messages.create(
        body="Python weather app notification: Today will rain",
        from_="+18888204408",
        to="+19709782102"
    )
    print(message.status)
else:
    message = client.messages.create(
        body="Python weather app notification: Today will not rain",
        from_="+18888204408",
        to="+19709782102"
    )
    print(message.status)
# print(weather_slice)







# print(data['hourly'][0]['weather'][0]['id'])

# print(hourly.head(12)['weather'])