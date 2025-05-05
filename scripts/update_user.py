#!/usr/bin/env python3
import os, sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv()

API_BASE   = os.getenv("API_BASE_URL", "https://api.macdonml.com")
EMAIL      = os.getenv("USER_EMAIL")
PASSWORD   = os.getenv("USER_PASSWORD")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

print(f"openai key:\n{OPENAI_KEY}")

if not EMAIL or not PASSWORD:
    print("❌ Please set USER_EMAIL and USER_PASSWORD in your .env", file=sys.stderr)
    sys.exit(1)

# 1) Log in to get a JWT
login = requests.post(
    f"{API_BASE}/token",
    data={"username": EMAIL, "password": PASSWORD},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print("LOGIN ➤", login.status_code, login.headers.get("Content-Type"))
try:
    print("LOGIN BODY:", login.json())
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))
login.raise_for_status()

token = login.json().get("access_token")
if not token:
    print("❌ No access_token in login response!", file=sys.stderr)
    sys.exit(1)

# 2) PATCH /users/me
patch = requests.patch(
    f"{API_BASE}/users/me",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    },
    json={
        "email":           EMAIL,
        "password":        PASSWORD,
        "openai_api_key":  OPENAI_KEY,
        "tavily_api_key":  TAVILY_KEY,
    },
)

print("PATCH ➤", patch.status_code, patch.headers.get("Content-Type"))
try:
    print("PATCH BODY:", patch.json())
except JSONDecodeError:
    print("PATCH BODY (raw):", repr(patch.text))

if patch.status_code >= 400:
    sys.exit(1)
