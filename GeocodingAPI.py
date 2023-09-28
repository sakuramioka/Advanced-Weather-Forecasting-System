import requests
import os
from dotenv import load_dotenv

#Get config files
load_dotenv()
MY_API_KEY = os.getenv("MY_API_KEY")

current_search_results = None

def get_geo_data(cityname, limit):
        global current_search_results
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit={limit}&appid={MY_API_KEY}")
        if response.status_code == 200:
            current_search_results = response.json()
            return current_search_results
        else:
            print(f"Hello, there's a {response.status_code} error with your request")
            return f"Fetch unsuccessful, returned error {response.status_code}."

def get_city_search_results():
    results = []
    if not current_search_results == None:
        for city in current_search_results:
            location = f"{city['name']}, {city['country']}"
            results.append(location)
        return results
    else:
        return []
    
def get_latitude(index = 0):
    if not current_search_results == None:
         return current_search_results[index]["lat"]
    else:
         return None

def get_longitude(index = 0):
    if not current_search_results == None:
         return current_search_results[index]["lon"]
    else:
         return None