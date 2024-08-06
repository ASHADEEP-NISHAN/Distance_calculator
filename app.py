import requests
from flask import Flask, render_template,request
from pprint import pprint
import uuid
import os

# Generate a UUIDv4
request_id = str(uuid.uuid4())

OLAMAP_ENDPOINT="https://api.olamaps.io"
#
# OLAMAP_APIKEY=os.environ.get("OLAMAP_APIKEY")
# client_id =os.environ.get("client_id")
# client_secret=os.environ.get("client_secret")

OLAMAP_APIKEY="PwRcI0Ag8RruNaim9FlwM6bbcawMlBiqE2RiVdAg"

# Replace with your actual client_id and client_secret
client_id = "0cad69ef-0e72-4f2d-8987-e7dda4a2ca42"
client_secret = "ApTKxofTrmmBJqQOOzAQMuKELOH0HFaI"

app=Flask(__name__)


# Get an access token
def access_token():
    token_url = "https://account.olamaps.io/realms/olamaps/protocol/openid-connect/token"
    token_data = {
        "grant_type": "client_credentials",
        "scope": "openid",
        "client_id": client_id,
        "client_secret": client_secret
    }
    token_response = requests.post(token_url, data=token_data)
    access_token = token_response.json().get("access_token")
    return access_token

# This is the access token
token=access_token()
headers = {
    "Authorization": f"Bearer {token}",
    "X-Request-Id": request_id
}
# Get coordinates
def get_coordinates(address:str):
    # geocoded of address
    Geocode_endpoint_url = f"{OLAMAP_ENDPOINT}/places/v1/geocode"
    query = {
        "address": address
    }
    response=requests.get(url=Geocode_endpoint_url,headers=headers,params=query)
    data=response.json()
    lat = data['geocodingResults'][0]['geometry']['location']['lat']
    lng = data['geocodingResults'][0]['geometry']['location']['lng']
    return lat,lng

# get the distance between two location
def distance(ORIGIN,DESTINATION):
    Direction_api = f"{OLAMAP_ENDPOINT}/routing/v1/directions"
    direction_query = {
        "origin": ORIGIN,
        "destination": DESTINATION
    }
    direction_response = requests.post(url=Direction_api, headers=headers, params=direction_query)
    direction_data = direction_response.json()
    pprint(direction_data)
    distance = direction_data['routes'][0]['legs'][0]['readable_distance']
    duration = direction_data['routes'][0]['legs'][0]['readable_duration']
    return distance,duration


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        origin_coordinates=get_coordinates(request.form['place1'])
        dest_coordinates=get_coordinates(request.form['place2'])
        origin=f"{origin_coordinates[0]},{origin_coordinates[1]}"
        destination=f"{dest_coordinates[0]},{dest_coordinates[1]}"
        calculate_distance=distance(ORIGIN=origin,DESTINATION=destination)
        return render_template("index.html", Calculate=True,Distance=calculate_distance[0],Duration=calculate_distance[1])
    else:
        return render_template("index.html", Calculate=False)

if __name__=="__main__":
    app.run(debug=True)