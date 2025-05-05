import os
import requests
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("API_PSWD")

url = "https://api.macdonml.com/token"
data = {
    "grant_type": "password",
    "username": "macdonc2@gmail.com",
    "password": PASSWORD,
    "scope": ""
}

response = requests.post(url, data=data)

if response.ok:
    token = response.json().get("access_token")
    print("Access Token:", token)
else:
    print("Failed to retrieve token:", response.status_code)
    print("Error:", response.text)