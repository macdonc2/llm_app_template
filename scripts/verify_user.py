import os
import sys
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

# Load .env
load_dotenv(override=True)

API_BASE        = os.getenv("API_BASE_URL",    "http://localhost:8000")
ADMIN_EMAIL     = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD  = os.getenv("ADMIN_PASSWORD")
USER_ID         = os.getenv("USER_ID_TO_VERIFY")

if not (ADMIN_EMAIL and ADMIN_PASSWORD and USER_ID):
    print("❌ Set ADMIN_EMAIL, ADMIN_PASSWORD and USER_ID_TO_VERIFY in .env", file=sys.stderr)
    sys.exit(1)

# 1) Login as superuser to get JWT
login = requests.post(
    f"{API_BASE}/auth/jwt/login",
    data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print("LOGIN  ➤", login.status_code)
try:
    lj = login.json(); print("LOGIN BODY:", lj)
except JSONDecodeError:
    print("LOGIN BODY (raw):", repr(login.text))
login.raise_for_status()

token = lj.get("access_token")
if not token:
    print("❌ No access_token returned!", file=sys.stderr)
    sys.exit(1)

# 2) Verify the user
resp = requests.post(
    f"{API_BASE}/admin/verify/{USER_ID}",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    },
)
print("VERIFY ➤", resp.status_code)
try:
    vj = resp.json(); print("VERIFY BODY:", vj)
except JSONDecodeError:
    print("VERIFY BODY (raw):", repr(resp.text))
resp.raise_for_status()
