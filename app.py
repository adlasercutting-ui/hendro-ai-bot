from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# CARA AMAN: Kita ambil kunci dari 'Environment Variable' di Render nanti
API_KEY = os.environ.get("GOOGLE_API_KEY") 
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('models/gemini-2.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pesan = data.get('message', '').lower()
        is_bos = "won ai aktif" in pesan or "ini hendro" in pesan
        status = "BOS HENDRO" if is_bos else "PELANGGAN"
        
        instruksi = f"Kamu Hendro AI, asisten AD LASER. User: {status}. Jawab ramah."
        response = model.generate_content(f"{instruksi}\n\nPesan: {pesan}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Aduh Bos, mesinnya lagi istirahat sebentar."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)