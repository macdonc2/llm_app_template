import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

# Load .env
load_dotenv(override=True)

API_BASE        = os.getenv("API_BASE_URL", "http://localhost:8000")
EMAIL           = os.getenv("USER_EMAIL")
PASSWORD        = os.getenv("USER_PASSWORD")
OPENAI_API_KEY  = os.getenv("USER_OPENAI_API_KEY")
TAVILY_API_KEY  = os.getenv("USER_TAVILY_API_KEY")

if not EMAIL or not PASSWORD:
    print("❌ Set USER_EMAIL and USER_PASSWORD in .env", file=sys.stderr)
    sys.exit(1)

payload = {
    "email": EMAIL,
    "password": PASSWORD,
}
if OPENAI_API_KEY:
    payload["openai_api_key"] = OPENAI_API_KEY
if TAVILY_API_KEY:
    payload["tavily_api_key"] = TAVILY_API_KEY

resp = requests.post(
    f"{API_BASE}/auth/register",
    json=payload,
    headers={"Content-Type": "application/json"},
)
print("REGISTER ➤", resp.status_code)
try:
    body = resp.json(); print("REGISTER BODY:", body)
except JSONDecodeError:
    print("REGISTER BODY (raw):", repr(resp.text))
resp.raise_for_status()
