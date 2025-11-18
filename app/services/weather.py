# app/services/weather.py

import requests


def fetch_weather(lat: float, lon: float):
   
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        print("[weather] Requesting:", url)
        response = requests.get(url, timeout=5)
        print("[weather] Status code:", response.status_code)
        print("[weather] Raw response:", response.text[:200])  # debug

        if response.status_code != 200:
            raise ValueError(f"Weather API failed: {response.status_code}")

        data = response.json()  # <-- THIS was failing

        if "current_weather" not in data:
            raise ValueError("Weather API returned no current_weather field")

        cw = data["current_weather"]
        return {
            "temperature": cw.get("temperature"),
            "windspeed": cw.get("windspeed"),
            "time": cw.get("time"),
        }

    except Exception as e:
        print("[weather] ERROR:", e)
        raise
