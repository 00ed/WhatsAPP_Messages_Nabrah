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

    user_phone = data.get('phone')  # e.g., 9665XXXXXXXX
    student_name = data.get('student_name')
    parent_name = data.get('parent_name')
    amount_due = data.get('amount_due')

    if not user_phone:
        return jsonify({"error": "Missing phone"}), 400

    # Auto-generate message if not provided
    message_text = data.get('message') or (
        f"أهلاً {parent_name}، يوجد مبلغ مستحق بقيمة {amount_due} ريال على الطالب {student_name}. لمزيد من التفاصيل أو المساعدة، تواصل معنا. مدارس القمم."
    )

    message = client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        to=f"whatsapp:+{user_phone}",
        body=message_text
    )

    return jsonify({"status": "sent", "sid": message.sid}), 200

@app.route('/pre-call', methods=['POST'])
def pre_call_callback():
    data = request.json
    student_id = data.get('student_id')

    # Example: simulate dynamic lookup
    if student_id == '001':
        return jsonify({
            "phone": "966502104776",
            "student_name": "Eyad",
            "parent_name": "Amer",
            "amount_due": 1200.5
        })
    elif student_id == '002':
        return jsonify({
            "phone": "966580323262",
            "student_name": "Mohammed",
            "parent_name": "Ahmad",
            "amount_due": 950
        })
    else:
        return jsonify({"error": "Student not found"}), 404
