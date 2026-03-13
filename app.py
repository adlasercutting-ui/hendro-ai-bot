from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Kunci API milik Bos Hendro
API_KEY = "AIzaSyD_g1QsDMEuXFWh5bGGHiposCFjVD2P6Dw"
genai.configure(api_key=API_KEY)

# Pakai model 2.5 yang sudah terbukti lancar di laptop Bos tadi
model = genai.GenerativeModel('models/gemini-2.5-flash')

# DATA BISNIS AD LASER & WON
HARGA_INFO = """
1. Akrilik 2mm: Rp 1.000 / cm
2. Akrilik 3mm: Rp 1.500 / cm
3. Akrilik 5mm: Rp 2.500 / cm
4. Kayu / MDF: Rp 800 / cm
5. Gravir: Rp 500 / cm2
Lokasi: Jakarta (AD LASER & WON)
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pesan_user = data.get('message', '').lower()
        
        # Logika Pintu Rahasia Bos Hendro
        is_bos = "won ai aktif" in pesan_user or "ini hendro" in pesan_user
        status = "BOS HENDRO" if is_bos else "PELANGGAN"

        instruksi = f"""
        Kamu adalah Hendro AI, asisten pintar AD LASER & WON.
        User saat ini: {status}.
        
        TUGAS:
        - Jika user adalah {status} (PELANGGAN), sapa 'Halo Kakak!'.
        - Gunakan harga ini: {HARGA_INFO}.
        - Jika ada ukuran (contoh 10x10cm), bantu hitung: P x L x Harga.
        - Jika user adalah BOS HENDRO, sapa 'Siap Bos Hendro!' dan jadilah asisten penurut.
        """
        
        response = model.generate_content(f"{instruksi}\n\nPesan: {pesan_user}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == '__main__':
    # Port wajib untuk server internet
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)