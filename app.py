from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import coqui_stt
import wave
import numpy as np

app = Flask(__name__)
CORS(app)  # CORS muammolarini hal qilish uchun

# Modelni yuklash
model_path = "model/model.tflite"
scorer_path = "model/scorer.scorer"
model = coqui_stt.Model(model_path)
model.enableExternalScorer(scorer_path)

# Matnga aylantirish endpoint
@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    try:
        # Audio faylni qabul qilish
        audio_file = request.files["audio"]
        with wave.open(audio_file, "rb") as wav_file:
            # WAVE formatni o‘qish
            frame_rate = wav_file.getframerate()
            frames = wav_file.readframes(wav_file.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
        
        # Matnga aylantirish
        text = model.stt(audio_data)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Frontend xizmat qilish
@app.route("/")
def index():
    return send_from_directory(directory="static", path="index.html")

if __name__ == "__main__":
    app.run(debug=True)
