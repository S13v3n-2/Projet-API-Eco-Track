def fetch_weather_data(lat=48.8566, lon=2.3522):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "past_days": 7
    }
    response = requests.get(url, params=params)
    return response.json()