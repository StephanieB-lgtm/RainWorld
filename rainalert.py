#TODO
# Get weather forecast API
# Create TWILIO ACCOUNT AND GET SID AND AUTHENTICATION TOKEN
# CHANGE "TO" TO YOUR NUMBER!


import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")

TWILIO_ACCOUNT_SID="YOURACCOUNT"
TWILIO_AUTH_TOKEN="YOURTOKEN"



parameters={
    "lat": 	59.930248, #OSLO, NORWAY
    "lon": 	10.732291,
    "exclude": "current,minutely,daily",
    "appid": api_key,
}

response=requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data=response.json()
weather_slice=weather_data["hourly"][:12]

will_rain=False

for hour_data in weather_slice:
    condition_code=hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain=True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,  http_client=proxy_client)

    message = client.messages.create(
        body="It is going to rain today. Remember to bring an umbrella! ☔",
        from_="+19362593268",
        to="YOUR NUMBER"
    )

    print(message.status)