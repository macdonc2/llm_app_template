#!/usr/bin/env python3
import os, sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv(override=True)

API_BASE = os.getenv("API_BASE_URL", "https://api.macdonml.com")
EMAIL    = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

print(EMAIL)
print(PASSWORD)

if not EMAIL or not PASSWORD:
    print("❌ Set USER_EMAIL and USER_PASSWORD in your .env", file=sys.stderr)
    sys.exit(1)

# 1) Hit /token, not /users
login = requests.post(
    f"{API_BASE}/token",
    data={
        "username": EMAIL,
        "password": PASSWORD,
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

print("LOGIN ➤", login.status_code, login.headers.get("Content-Type"))
try:
    print("LOGIN BODY:", login.json())
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))

if not login.ok:
    sys.exit(1)

token = login.json().get("access_token")
if not token:
    print("❌ No access_token in login response!", file=sys.stderr)
    sys.exit(1)

print("✅ Retrieved token:", token)
