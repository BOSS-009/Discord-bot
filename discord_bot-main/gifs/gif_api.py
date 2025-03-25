
# *** simple moduel for getting gif's from tenor api ***

import json
import random
import requests 

async def get_gif(api_key = "your_api_key" , gif_name = "defult"):
    try:

        # max gif's from response
        max_gifs_request = 20

        # pick random one
        index = random.randint(0,max_gifs_request-1)

        # send requst & get gif url
        response = requests.get( "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (gif_name, api_key , max_gifs_request) )
        
        # respone code '200' mean all is good  
        if response.status_code == 200 :
            # parse response content
            data = json.loads(response.content)["results"]

            # pick random gif & send it 
            return ( data[index]["media"][0]["gif"]["url"] )

        else : # mean error happend in request or response 
            return "possible request/response error"

    # if any exception happend we must raise it + error message
    except Exception as err:
        raise "[!gif] " + err
