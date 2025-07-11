from flask import Flask, request, jsonify
from twilio.rest import Client
import os
import json
import requests

app = Flask(__name__)

# Load credentials from environment variables (for Render)
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
FROM_WHATSAPP_NUMBER = os.environ.get('FROM_WHATSAPP', 'whatsapp:+14155238886')

# Load credentials from environment variables (for Hugging Face)
HF_API_KEY = os.environ.get('HF_API_KEY')
HF_MODEL_URL = os.environ.get('HF_MODEL_URL', 'https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli')
HF_headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def home():
    return "✅ WhatsApp Callback API is running!"

@app.route('/post-call', methods=['POST'])
def post_call_callback():
    print("=== Post-Call Triggered ===")
    data = request.json

    print("Received Data:", data)

    # Step 1: Parse the nested JSON string
    call_data = json.loads(data.get("call_details", "{}"))

    # Step 2: Extract variables from it
    variables = call_data.get("variables", {})
    user_phone = variables.get("phone")
    parent_name = variables.get("parent_name")
    student_name = variables.get("student_name")
    amount_due = variables.get("amount_due")

    print("Phone:", user_phone)
    print("Parent:", parent_name)
    print("Student:", student_name)
    print("Amount Due:", amount_due)

    # Normalize phone number (make sure it starts with +)
    if not str(user_phone).startswith('+'):
        user_phone = f"+{user_phone}"

    # Check for missing phone
    if not user_phone:
        print("❌ Error: Missing phone number!")
        return jsonify({"error": "Missing phone"}), 400

    # Generate message if not provided
    message_text = (
        data.get('message') or
        f"أهلاً {parent_name}، يوجد مبلغ مستحق بقيمة {amount_due} ريال على الطالب {student_name}. لمزيد من التفاصيل أو المساعدة، تواصل معنا. مدارس القمم."
    )

    print(f"📤 Final WhatsApp Message: {message_text}")
    print(f"📞 Sending to: whatsapp:{user_phone}")

    # Send message via Twilio
    try:
        message = client.messages.create(
            from_=FROM_WHATSAPP_NUMBER,
            to=f"whatsapp:{user_phone}",
            body=message_text
        )
    except Exception as e:
        print("❌ Error sending WhatsApp message:", e)
        return jsonify({"error": str(e)}), 500


    print("✅ Message sent successfully!")
    print(f"Twilio SID: {message.sid}")
    return jsonify({"status": "sent", "sid": message.sid}), 200


@app.route('/pre-call', methods=['POST'])
def pre_call_callback():
    print("=== Pre-Call Triggered ===")
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
            "amount_due": 1200
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


@app.route('/post-analysis', methods=['POST'])
def post_analysis_callback():
    print("=== Post-Analysis Triggered ===")

    data = request.json
    call_details = json.loads(data.get("call_details", "{}"))

    transcript = call_details.get("transcript", [])
    full_text = " ".join([turn['message'] for turn in transcript])

    # Send to Hugging Face for sentiment analysis
    response = requests.post(HF_MODEL_URL, headers=HF_headers, json={
        "inputs": full_text,
        "parameters": {
            "candidate_labels": ["مهذب", "غاضب", "مرتبك", "مهتم", "مستعجل", "محايد", "مشوش"]
        }
    })
    
    # Debug if response is empty or invalid
    print("📋 Status code:", response.status_code)
    
    try:
        result = response.json()
        print("📊 Analysis Result:", result)
        
    except Exception as e:
        print("❌ Failed to parse response JSON:", e)
        return jsonify({"error": str(e)}), 500

    top_label = result['labels'][0]
    confidence = round(result['scores'][0] * 100, 2)
    print(f"🧠 Most likely label: {top_label} ({confidence}%)")
    
    # You can also store or forward this analysis as needed
    return jsonify({"analysis": result}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render will set PORT env var
    app.run(host='0.0.0.0', port=port)
