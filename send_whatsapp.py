from twilio.rest import Client

# Twilio credentials (from https://console.twilio.com/)
ACCOUNT_SID = 'AC91ec67ed1d000b4c4cf23453e65c4072'
AUTH_TOKEN = '82bdf5d8f3c2648d00b2bc21e34d581f'

# Twilio Sandbox WhatsApp number
FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
TO_WHATSAPP_NUMBER = 'whatsapp:+966502104776'  # user phone number

def send_whatsapp_message(body_text):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        to=TO_WHATSAPP_NUMBER,
        body=body_text
    )

    print(f"Message sent! SID: {message.sid}")

# Example usage
send_whatsapp_message("✅ Your voice call has been completed. Thank you!")
