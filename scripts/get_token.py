import os
import requests
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("USER_PASSWORD")

url = "http://rag-api/token"
data = {
    "username": "macdonc2@gmail.com",
    "password": PASSWORD,
    "grant_type": "password",
    "scope": ""
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=data, headers=headers)

if response.ok:
    token = response.json().get("access_token")
    print("Access Token:", token)
else:
    print("Failed to retrieve token:", response.status_code)
    print("Error:", response.text)
