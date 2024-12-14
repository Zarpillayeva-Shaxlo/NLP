import streamlit as st
import os
import numpy as np
import wave
import tempfile
from stt import Model

# Global model variable
model = None

def load_model():
    """Load the STT model."""
    global model
    if model is None:
        model_path = "models/coqui-stt-model.tflite"
        scorer_path = "models/huge-vocabulary.scorer"

        if not os.path.exists(model_path):
            st.error("Model file not found. Please ensure the model is correctly placed.")
            return None

        model = Model(model_path)

        if os.path.exists(scorer_path):
            model.enableExternalScorer(scorer_path)
        else:
            st.warning("Scorer file not found. Using model without scorer.")

    return model

def transcribe_audio(file_path):
    """Transcribe the audio file using the STT model."""
    model = load_model()
    if not model:
        return ""

    with wave.open(file_path, 'rb') as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
            st.error("Audio file must be WAV format mono PCM.")
            return ""

        audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16)
        text = model.stt(audio)
        return text

def main():
    st.title("Speech-to-Text Application")
    st.write("Upload an audio file or record using your microphone, and we'll transcribe it for you.")

    model_status = "Loaded" if model else "Not Loaded"
    st.sidebar.write(f"Model Status: {model_status}")

    uploaded_file = st.file_uploader("Upload an audio file (WAV format only)", type="wav")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_file_path = temp_audio.name

        st.audio(uploaded_file, format='audio/wav')
        transcription = transcribe_audio(temp_file_path)
        if transcription:
            st.success("Transcription completed successfully!")
            st.text_area("Transcribed Text", transcription, height=200)

    if st.button("Test Microphone Recording"):
        st.info("Microphone recording feature can be added using additional libraries like 'pyaudio' or 'speech_recognition'.")

if __name__ == "__main__":
    main()
