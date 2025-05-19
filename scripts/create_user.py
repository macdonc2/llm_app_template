import os
import requests
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
PASSWORD = os.getenv("USER_PASSWORD")

url = "https://api.macdonml.com/users/"
# url = "http://rag-api/users/"
headers = {
    "Content-Type": "application/json"
}
data = {
    "email": "macdonc2@gmail.com",
    "password": PASSWORD,
    "openai_api_key": openai_key
}

response = requests.post(url, headers=headers, json=data)
print("User creation status:", response.status_code)
print("Response:", response.json())