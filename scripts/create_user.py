import os
import requests
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

url = "https://api.macdonml.com/users/"
headers = {
    "Content-Type": "application/json"
}
data = {
    "email": "macdonc2@gmail.com",
    "password": "Guitar0120!",
    "openai_api_key": openai_key
}

response = requests.post(url, headers=headers, json=data)
print("User creation status:", response.status_code)
print("Response:", response.json())