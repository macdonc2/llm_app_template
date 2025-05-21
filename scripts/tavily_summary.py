import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv(override=True)

# Point to your local server by default
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
EMAIL    = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

# You can override these in .env without touching the script:
QUERY = os.getenv("TAVILY_QUERY", "latest AI news")
TOP_K = int(os.getenv("TAVILY_TOP_K", "5"))

if not EMAIL or not PASSWORD:
    print("❌ Please set USER_EMAIL and USER_PASSWORD in your .env", file=sys.stderr)
    sys.exit(1)

# 1) Authenticate
login = requests.post(
    f"{API_BASE}/auth/jwt/login",
    data={"username": EMAIL, "password": PASSWORD},
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept":       "application/json",
    },
)
print("LOGIN   ➤", login.status_code)
try:
    body = login.json()
    print("LOGIN BODY:", body)
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))
login.raise_for_status()

token = body.get("access_token")
if not token:
    print("❌ No access_token in login response!", file=sys.stderr)
    sys.exit(1)

# 2) Call /tavily/summarize
payload = {
    "query": QUERY,
    "top_k": TOP_K,
}

resp = requests.post(
    f"{API_BASE}/tavily/summarize",
    json=payload,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    },
)
print("SUMMARIZE ➤", resp.status_code)
try:
    print("SUMMARIZE BODY:", resp.json())
except JSONDecodeError:
    print("SUMMARIZE BODY (raw):", repr(resp.text))

if resp.status_code >= 400:
    sys.exit(1)