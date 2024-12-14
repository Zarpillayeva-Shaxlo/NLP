# app.py - Streamlit ilova kodi
import streamlit as st
import deepspeech
import wave
import numpy as np

# Model fayllari yo'li
MODEL_FILE = "deepspeech-0.9.3-models.pbmm"
SCORER_FILE = "deepspeech-0.9.3-models.scorer"

# DeepSpeech modelini yuklash
@st.cache_resource
def load_model():
    model = deepspeech.Model(MODEL_FILE)
    model.enableExternalScorer(SCORER_FILE)
    return model

model = load_model()

# Ovoz faylini o'qish funksiyasi
def read_audio(file):
    with wave.open(file, "rb") as wf:
        rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)
        return audio, rate

# Streamlit interfeysi
st.title("DeepSpeech Ovozdan Matnga Ilovasi")
st.write("Mozilla DeepSpeech modeli yordamida ovozni matnga aylantirish!")

# Audio yuklash
uploaded_file = st.file_uploader("Ovoz faylini yuklang (.wav formatda)", type=["wav"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    audio, rate = read_audio(uploaded_file)
    
    # Transkriptsiya qilish
    with st.spinner("Transkripsiya qilinmoqda..."):
        text = model.stt(audio)
    st.success("Transkripsiya tugadi!")
    st.write("**Matn:**")
    st.write(text)




