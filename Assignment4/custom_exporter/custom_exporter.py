from prometheus_client import start_http_server, Gauge
import requests, time, random

# Define Prometheus metrics
temperature = Gauge('weather_temperature_celsius', 'Temperature in Celsius')
wind_speed = Gauge('weather_wind_speed_mps', 'Wind speed in m/s')
humidity = Gauge('weather_humidity_percent', 'Humidity percentage')

# Set your desired coordinates
LATITUDE = 51.11
LONGITUDE = 71.46

def fetch_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        response = requests.get(url, timeout=10)
        data = response.json().get('current_weather', {})

        if not data:
            print("No weather data returned")
            return

        # Add small random variation for testing dynamic metrics
        temperature.set(data['temperature'] + random.uniform(-0.5, 0.5))
        wind_speed.set(data['windspeed'] + random.uniform(-0.2, 0.2))
        humidity.set(random.uniform(40, 80))  # Simulate humidity 40-80%

        print(f"Updated metrics: Temp={temperature._value.get():.2f}°C, Wind={wind_speed._value.get():.2f} m/s, Humidity={humidity._value.get():.1f}%")

    except Exception as e:
        print("Error fetching weather:", e)

if __name__ == "__main__":
    # Start Prometheus metrics server on port 9200
    start_http_server(9200)
    print("✅ Custom Exporter running on port 9200")
    
    while True:
        fetch_weather()
        time.sleep(10)
