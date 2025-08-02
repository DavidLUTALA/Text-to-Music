import os
import torch
import streamlit as st
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np
from tempfile import NamedTemporaryFile
import base64

# Pour corriger les erreurs liées à torch.load
torch.serialization.add_safe_globals([np.core.multiarray.scalar])

@st.cache_resource
def load_bark_models():
    with st.spinner("🔧 Chargement des modèles Bark..."):
        preload_models()
    return True

def synthesize(text: str) -> str:
    st.info("🎼 Génération de l'audio en cours...")
    audio_array = generate_audio(text)
    output_path = save_audio(audio_array)
    return output_path

def save_audio(audio_array):
    with NamedTemporaryFile(delete=False, suffix=".wav", dir=".") as f:
        write_wav(f.name, SAMPLE_RATE, audio_array)
        return f.name

def download_button(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="generated_audio.wav">🎵 Télécharger le fichier audio</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Text-to-Music with Bark", layout="centered")
    st.title("🎤 Texte vers Audio avec Bark (Suno)")

    if load_bark_models():
        text_input = st.text_area("Entrez votre texte :", height=150, placeholder="Exemple : Hello world, this is Bark speaking...")
        if st.button("🎧 Générer l'audio"):
            if text_input.strip() != "":
                audio_path = synthesize(text_input)
                st.audio(audio_path, format="audio/wav")
                download_button(audio_path)
            else:
                st.warning("⛔ Veuillez entrer un texte valide.")

if __name__ == "__main__":
    main()
