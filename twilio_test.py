from twilio.rest import Client

account_sid = "AC633788f6bd76658fd83fef9989c93c45"
auth_token = "b5e542d925c68b5bf9006689357fe047"
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_="whatsapp:+14155238886",   # Twilio sandbox number
    body="Hello 👋, this is a test message from Python script via Twilio!",
    to="whatsapp:+919657712024"      # yaha apna WhatsApp number likho
)

print("Message SID:", message.sid)
