import requests

lat = 11.0018115
lon = 76.9628425

current_weather_results = None

def get_forecast(latitude, longitude, hourly_parameters, daily_parameters, time_mode):
        global current_weather_results
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly={hourly_parameters}&daily={daily_parameters}&timezone={time_mode}")
        if response.status_code == 200:
            current_weather_results = response.json()
            return current_weather_results
        else:
            print(f"Hello, there's a {response.status_code} error with your request")
            return f"Fetch unsuccessful, returned error {response.status_code}."