#!/usr/bin/env python3
import os, sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

# 1) Load .env (override any existing values so our .env keys actually take effect)
load_dotenv(override=True)

API_BASE       = os.getenv("API_BASE_URL", "https://api.macdonml.com")
EMAIL          = os.getenv("USER_EMAIL")
PASSWORD       = os.getenv("USER_PASSWORD")
OPENAI_KEY     = os.getenv("OPENAI_API_KEY")
TAVILY_KEY     = os.getenv("TAVILY_API_KEY")
FIRECRAWL_KEY  = os.getenv("FIRECRAWL_API_KEY")

if not EMAIL or not PASSWORD:
    print("❌ Please set USER_EMAIL and USER_PASSWORD in your .env", file=sys.stderr)
    sys.exit(1)

print("🔑 OpenAI key loaded:", OPENAI_KEY)

# 2) Log in—hit the FastAPI-Users JWT login endpoint, not /token
login = requests.post(
    f"{API_BASE}/auth/jwt/login",
    data={"username": EMAIL, "password": PASSWORD},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print("LOGIN ➤", login.status_code)
try:
    login_data = login.json()
    print("LOGIN BODY:", login_data)
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))
login.raise_for_status()

token = login_data.get("access_token")
if not token:
    print("❌ No access_token in login response!", file=sys.stderr)
    sys.exit(1)

# 3) PATCH /users/me with your new API keys
payload = {
    "email":              EMAIL,
    "password":           PASSWORD,
    "openai_api_key":     OPENAI_KEY,
    "tavily_api_key":     TAVILY_KEY,
    "firecrawl_api_key":  FIRECRAWL_KEY,
}
patch = requests.patch(
    f"{API_BASE}/users/me",
    json=payload,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    },
)
print("PATCH ➤", patch.status_code)
try:
    print("PATCH BODY:", patch.json())
except JSONDecodeError:
    print("PATCH BODY (raw):", repr(patch.text))
patch.raise_for_status()
