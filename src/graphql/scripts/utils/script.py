import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get App Credentials from .env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Tokens to exchange (loaded from .env)
tokens = {
    "PAGE_1": os.getenv("SHORT_TOKEN_1"),
    "PAGE_2": os.getenv("SHORT_TOKEN_2")
}

def exchange_token(short_token):
    """Exchange a short-lived token for a long-lived token."""
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_token
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Error exchanging token:", response.json())
        return None

# Store long-lived tokens
long_lived_tokens = {}

for page, short_token in tokens.items():
    if short_token:
        long_lived_token = exchange_token(short_token)
        if long_lived_token:
            long_lived_tokens[page] = long_lived_token
            print(f"✅ Long-lived token for {page}: {long_lived_token}")

# Update .env file with long-lived tokens
if long_lived_tokens:
    with open(".env", "a") as env_file:
        for page, token in long_lived_tokens.items():
            env_file.write(f"\nLONG_{page}={token}")

    print("\n✅ .env file updated with long-lived tokens.")