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

    # Extract data
    user_phone = data.get('phone')          # e.g., 9665XXXXXXXX
    student_name = data.get('student_name')
    parent_name = data.get('parent_name')
    amount_due = data.get('amount_due')
    message_text = data.get('message')

    # === Debug logs ===
    print("=== Post-Call Triggered ===")
    print(f"Received Data: {data}")
    print(f"Phone: {user_phone}")
    print(f"Parent: {parent_name}")
    print(f"Student: {student_name}")
    print(f"Amount Due: {amount_due}")
    print(f"Message Provided?: {'Yes' if message_text else 'No'}")

    # Check for missing phone
    if not user_phone:
        print("❌ Error: Missing phone number!")
        return jsonify({"error": "Missing phone"}), 400

    # Generate message if not provided
    message_text = message_text or (
        f"أهلاً {parent_name}، يوجد مبلغ مستحق بقيمة {amount_due} ريال على الطالب {student_name}. "
        f"لمزيد من التفاصيل أو المساعدة، تواصل معنا. مدارس القمم."
    )

    print(f"📤 Final WhatsApp Message: {message_text}")
    print(f"📞 Sending to: whatsapp:+{user_phone}")

    # Send message via Twilio
    message = client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        to=f"whatsapp:+{user_phone}",
        body=message_text
    )

    print("✅ Message sent successfully!")
    print(f"Twilio SID: {message.sid}")
    return jsonify({"status": "sent", "sid": message.sid}), 200


@app.route('/pre-call', methods=['POST'])
def pre_call_callback():
    data = request.json
    student_id = data.get('student_id')
    print(f"Received pre-call for student_id: {student_id}")  # Log input

    # Example: simulate dynamic lookup
    if student_id == '001':
        print("✅ student 001 pass")
        return jsonify({
            "phone": "966502104776",
            "student_name": "Eyad",
            "parent_name": "Amer",
            "amount_due": 1200.5
        })
    elif student_id == '002':
        print("✅ student 002 pass")
        return jsonify({
            "phone": "966580323262",
            "student_name": "Mohammed",
            "parent_name": "Ahmad",
            "amount_due": 950
        })
    else:
        print("❌ Unknown student_id")
        return jsonify({"error": "Student not found"}), 404
