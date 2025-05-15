#!/usr/bin/env python3
import os, sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv()

API_BASE   = os.getenv("API_BASE_URL", "https://api.macdonml.com")
EMAIL      = os.getenv("USER_EMAIL")
PASSWORD   = os.getenv("USER_PASSWORD")

# You can override these to test different queries without changing the script:
QUERY  = os.getenv("TAVILY_QUERY", "latest AI news")  
TOP_K  = int(os.getenv("TAVILY_TOP_K", "5"))

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

# 2) POST /tavily/summarize
payload = {
    "query": QUERY,
    "top_k": TOP_K,
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type":  "application/json",
}

resp = requests.post(
    f"{API_BASE}/tavily/summarize",
    headers=headers,
    json=payload,
)

print("SUMMARIZE ➤", resp.status_code, resp.headers.get("Content-Type"))
try:
    print("SUMMARIZE BODY:", resp.json())
except JSONDecodeError:
    print("SUMMARIZE BODY (raw):", repr(resp.text))

if resp.status_code >= 400:
    sys.exit(1)
