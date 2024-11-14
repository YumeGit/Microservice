# email_service.py
import resend
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Устанавливаем API ключ из .env
resend.api_key = os.getenv("RESEND_API_KEY")
port = os.getenv("PORT", 5001)

def send_email(from_address, to_address, subject, html_content):
    """Отправляет email через Resend API."""
    try:
        response = resend.Emails.send({
            "from": from_address,
            "to": to_address,
            "subject": subject,
            "html": html_content
        })
        return response
    except Exception as e:
        return str(e)

@app.route('/send-email', methods=['POST'])
def send_email_route():
    """Endpoint для отправки email. Ожидает JSON с полями: from, to, subject, html."""
    data = request.json
    required_fields = {"from", "to", "subject", "html"}
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    from_address = data["from"]
    to_address = data["to"]
    subject = data["subject"]
    html_content = data["html"]
    
    # Отправка email через Resend API
    result = send_email(from_address, to_address, subject, html_content)
    
    if isinstance(result, str):
        return jsonify({"error": result}), 500
    
    return jsonify({"message": "Email sent successfully", "response": result}), 200

if __name__ == '__main__':
    from waitress import serve
    print(f"Running server at 0.0.0.0:{port}");
    serve(app, host="0.0.0.0", port=port)