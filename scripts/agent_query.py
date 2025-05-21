import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

# Load .env
load_dotenv(override=True)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
EMAIL    = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")
QUERY    = os.getenv("AGENT_QUERY", "What is 2 + 2?")

if not EMAIL or not PASSWORD:
    print("❌ Set USER_EMAIL and USER_PASSWORD in .env", file=sys.stderr)
    sys.exit(1)

# 1) Get JWT
login = requests.post(
    f"{API_BASE}/auth/jwt/login",
    data={"username": EMAIL, "password": PASSWORD},
    headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
)
print("LOGIN ➤", login.status_code)
try:
    j = login.json(); print("LOGIN BODY:", j)
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))
login.raise_for_status()

token = j.get("access_token")
if not token:
    print("❌ No access_token!", file=sys.stderr)
    sys.exit(1)

# 2) Call /agent/ask
resp = requests.post(
    f"{API_BASE}/agent/ask",
    json={"query": QUERY},
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    },
)
print("AGENT ➤", resp.status_code)
try:
    aj = resp.json(); print("AGENT BODY:", aj)
except JSONDecodeError:
    print("AGENT BODY (raw):", repr(resp.text))
resp.raise_for_status()

print("Agent says:", aj.get("response"))