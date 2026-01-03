import requests

API_KEY = "ec8d8b2b7545db7ad30b9056444928cd"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
AQI_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


def get_weather(city):
    params = {
        "q": city + ",IN",
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(WEATHER_URL, params=params)
    data = response.json()

    if str(data.get("cod")) != "200":
        return None

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].capitalize(),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"]
    }


def get_aqi(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    response = requests.get(AQI_URL, params=params)
    data = response.json()

    aqi = data["list"][0]["main"]["aqi"]
    return aqi


def aqi_health_message(aqi):
    messages = {
        1: "Good 😊 – Air quality is satisfactory.",
        2: "Fair 🙂 – Acceptable air quality.",
        3: "Moderate 😐 – Sensitive people should be cautious.",
        4: "Poor 😷 – Avoid outdoor activities.",
        5: "Very Poor 🚫 – Health warnings for everyone."
    }
    return messages.get(aqi, "No data available")


def main():
    city = input("Enter city name: ").strip()

    weather = get_weather(city)
    if not weather:
        print("❌ City not found or API issue!")
        return

    aqi = get_aqi(weather["lat"], weather["lon"])

    print("\n🌦️ Weather Report")
    print("----------------------")
    print(f"City        : {weather['city']}")
    print(f"Temperature : {weather['temp']}°C")
    print(f"Humidity    : {weather['humidity']}%")
    print(f"Condition   : {weather['condition']}")

    print("\n😷 Air Quality Index (AQI)")
    print("----------------------")
    print(f"AQI Level   : {aqi}")
    print(f"Health Tip  : {aqi_health_message(aqi)}")


if __name__ == "__main__":
    main()
