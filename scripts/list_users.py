import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

# Load .env
load_dotenv(override=True)

API_BASE       = os.getenv("API_BASE_URL",    "http://localhost:8000")
ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not (ADMIN_EMAIL and ADMIN_PASSWORD):
    print("❌ Set ADMIN_EMAIL and ADMIN_PASSWORD in .env", file=sys.stderr)
    sys.exit(1)

# 1) Login as superuser to get JWT
auth_resp = requests.post(
    f"{API_BASE}/auth/jwt/login",
    data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print("LOGIN   ➤", auth_resp.status_code)
try:
    auth_json = auth_resp.json(); print("LOGIN BODY:", auth_json)
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(auth_resp.text))
auth_resp.raise_for_status()

token = auth_json.get("access_token")
if not token:
    print("❌ No access_token returned!", file=sys.stderr)
    sys.exit(1)

# 2) List all users as superuser
list_resp = requests.get(
    f"{API_BASE}/admin/users",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept":        "application/json",
    },
)
print("USERS   ➤", list_resp.status_code)
try:
    users = list_resp.json(); print("USERS BODY:", users)
except JSONDecodeError:
    print("USERS BODY (raw):", repr(list_resp.text))
list_resp.raise_for_status()
