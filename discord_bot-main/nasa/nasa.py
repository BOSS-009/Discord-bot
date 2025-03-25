import requests
import json

def get_photo(nasa_url , api_key) :

    req = requests.get(nasa_url+api_key)

    if req.status_code == 200:
        return json.loads(req.content)["url"]
    
    else:
        return ("Bad Conncetion to Nasa API's")

def get_description(nasa_url , api_key):
    req = requests.get(nasa_url+api_key)

    if req.status_code == 200:
        return json.loads(req.content)["explanation"]
       
    else:
        return ("Bad Conncetion to Nasa API's")