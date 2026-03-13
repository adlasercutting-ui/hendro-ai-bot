from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Ambil dari Environment Variable Render agar aman
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pesan = data.get('message', '').lower()
        
        # Pintu Rahasia Bos Hendro
        is_bos = "won ai aktif" in pesan or "ini hendro" in pesan
        status = "BOS HENDRO" if is_bos else "PELANGGAN"

        instruksi = f"""
        Kamu adalah Hendro AI, asisten pintar AD LASER & WON.
        Status User: {status}.
        - Jika PELANGGAN: Sapa 'Halo Kakak!'. Berikan harga: Akrilik 2mm (1rb), 3mm (1.5rb), 5mm (2.5rb) per cm.
        - Jika BOS HENDRO: Sapa 'Siap Bos Hendro!' dan jadilah penurut.
        """
        
        response = model.generate_content(f"{instruksi}\n\nPesan: {pesan}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Mesin lagi cooling down, Bos!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
