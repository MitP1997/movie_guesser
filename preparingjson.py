import urllib
import requests
import json

url1 = "http://api.themoviedb.org/3/movie/"
url2 = "?api_key=573960af652e25f99356d4bf4c14d987"
#341030
for i in range(0,100):
    print i
    r = requests.get(url1+str(i)+url2, None)
    x = r.json()
    try:
        x["status_code"]
    except KeyError:
        pass
