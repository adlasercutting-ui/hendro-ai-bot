from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
# CORS ini penting supaya website Hostinger bisa ngobrol sama Render
CORS(app)

# Ambil kunci dari brankas Render (lebih aman!)
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- DATA BISNIS AD LASER ---
PRICELIST = """
1. Akrilik 2mm: Rp 1.000 / cm
2. Akrilik 3mm: Rp 1.500 / cm
3. Akrilik 5mm: Rp 2.500 / cm
4. Kayu / MDF: Rp 800 / cm
5. Gravir: Rp 500 / cm2
Minimal Order: Rp 50.000
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pesan_user = data.get('message', '').lower()
        
        # Cek siapa yang bicara
        is_bos = "won ai aktif" in pesan_user or "ini hendro" in pesan_user
        status = "BOS HENDRO" if is_bos else "PELANGGAN"

        instruksi = f"""
        Kamu adalah Hendro AI, asisten pintar AD LASER & WON.
        User saat ini: {status}.
        
        - Jika PELANGGAN: Sapa 'Halo Kakak!'. Berikan info harga: {PRICELIST}. 
        - Jika ada ukuran (misal 10x20), bantu hitung: P x L x Harga.
        - Jika BOS HENDRO: Sapa 'Siap Bos Hendro!' dan jadilah asisten sangat patuh.
        - Selalu tanyakan apakah file sudah siap cetak atau perlu jasa desain.
        """
        
        response = model.generate_content(f"{instruksi}\n\nPesan: {pesan_user}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Aduh Bos, mesin lagi panas. Coba sebentar lagi ya!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)