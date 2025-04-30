import requests

url = "https://api.macdonml.com/token"
data = {
    "grant_type": "password",
    "username": "user@email.com",
    "password": "Secretkey",
    "scope": ""
}

response = requests.post(url, data=data)

if response.ok:
    token = response.json().get("access_token")
    print("Access Token:", token)
else:
    print("Failed to retrieve token:", response.status_code)
    print("Error:", response.text)