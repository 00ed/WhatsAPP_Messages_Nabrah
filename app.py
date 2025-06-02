from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Load credentials (use env variables in production)
ACCOUNT_SID = 'AC91ec67ed1d000b4c4cf23453e65c4072'
AUTH_TOKEN = '82bdf5d8f3c2648d00b2bc21e34d581f'
FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio sandbox number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/post-call', methods=['POST'])
def post_call_callback():
    data = request.json

    user_phone = data.get('phone')   # e.g., 9665XXXXXXXX
    message_text = data.get('message', '✅ Your AI call is complete. Thank you!')

    if not user_phone:
        return jsonify({"error": "Missing phone"}), 400

    message = client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        to=f"whatsapp:+{user_phone}",
        body=message_text
    )

    return jsonify({"status": "sent", "sid": message.sid}), 200

if __name__ == "__main__":
    app.run(port=5000)
