import json
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

# === CONFIG ===
SERVICE_ACCOUNT_FILE = "C:/Users/Admin/Downloads/charged-garden-427305-h3-0e991ea6b82e.json"
SCOPES = ["https://www.googleapis.com/auth/business.manage"]

# Replace with your actual IDs (must be numeric, not Place IDs)
ACCOUNT_ID = "7381-5972-2785-3096-980"      # Your Business Account ID
LOCATION_ID = "ChIJ9Yw2ruq_wjsRjcPfsQ6gNS8"      # Your Business Location ID
     # Review ID you want to reply to

# === AUTHENTICATION ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Use correct Business Reviews API
service = build("mybusinessreviews", "v1", credentials=credentials)

# === PREPARE REPLY BODY ===
reply_body = {
    "comment": "Thank you for your review! We appreciate your feedback."
}

# === REPLY TO REVIEW ===
try:
    review_name = f"accounts/{ACCOUNT_ID}/locations/{LOCATION_ID}/reviews/{REVIEW_ID}"
    response = service.accounts().locations().reviews().updateReply(
        name=review_name,
        body=reply_body
    ).execute()

    print("✅ Reply posted successfully!")
    print(json.dumps(response, indent=2))

except Exception as e:
    print("❌ Failed to post reply:", e)
