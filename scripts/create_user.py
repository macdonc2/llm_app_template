import requests

url = "https://api.macdonml.com/users/"
headers = {
    "Content-Type": "application/json"
}
data = {
    "email": "user@email.com",
    "password": "Secretkey",
    "openai_api_key": "sk-proj-personalkey"
}

response = requests.post(url, headers=headers, json=data)
print("User creation status:", response.status_code)
print("Response:", response.json())