from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Load credentials from environment variables (for Render)
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
FROM_WHATSAPP_NUMBER = os.environ.get('FROM_WHATSAPP', 'whatsapp:+14155238886')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def home():
    return "✅ WhatsApp Callback API is running!"

@app.route('/post-call', methods=['POST'])
def post_call_callback():
    data = request.json

    user_phone = data.get('phone')   # e.g., 9665XXXXXXXX
    message_text = data.get('message', '✅ Your AI call is complete.\nHi {{student_name}}, thank you for speaking with us. Your due amount is {{amount_due}} SAR.')

    if not user_phone:
        return jsonify({"error": "Missing phone"}), 400

    message = client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        to=f"whatsapp:+{user_phone}",
        body=message_text
    )

    return jsonify({"status": "sent", "sid": message.sid}), 200

@app.route('/pre-call', methods=['POST'])
def pre_call_callback():
    # Example: return dynamic or fixed values for the voice agent to use
    return jsonify({
        "phone": "966502104776",
        "student_name": "Mohammed",
        "amount_due": 1200.5
    })
