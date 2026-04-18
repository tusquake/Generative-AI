import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = "98a420bf4dc2e3a519647b8fba94d2ed"
city = "Bangalore"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
