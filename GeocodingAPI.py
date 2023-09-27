import requests

MY_API_KEY = 'da5324df0dddcd4be49d5e59233a1e5a'
current_search_results = None

def get_geo_data(cityname, limit):
        global current_search_results
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit={limit}&appid={MY_API_KEY}")
        if response.status_code == 200:
            current_search_results = response.json()
            return "Fetch successful!"
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
    
success = get_geo_data("London", 5)
results = get_city_search_results()
lat = get_latitude()
long = get_longitude()

print(success)
print(results)
print(lat)
print(long)