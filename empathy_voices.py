import streamlit as st
import tempfile
import os
from elevenlabs import ElevenLabs

# Initialize ElevenLabs client
eleven_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Page config and theme colors
st.set_page_config(page_title="Empathy Voices", layout="centered")

st.markdown(
    """
    <style>
        body {
            font-family: 'Helvetica Neue', sans-serif;
        }
        .stApp {
            background-color: #f8fdf8;
        }
        .title {
            color: #03aa00;
            text-align: center;
            font-size: 2em;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #2092f7;
            font-size: 1.1em;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">Empathy Voices</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bring warmth and humanity back to digital speech</div>', unsafe_allow_html=True)
st.write("")

# Text input
text_input = st.text_area("📝 Enter text to bring to life:", height=150)

# Voice options mapped to your specific IDs
voices = {
    "💛 Comforting Friend": "6aDn1KB0hjpdcocrUkmq",
    "🔥 Motivational Coach": "bTEswxYhpv7UDkQg5VRu",
    "👵🏽 Wise Grandmother": "0rEo3eAjssGDUCXHYENf",
}

# Dropdown for voice tone
selected_label = st.selectbox("🎙️ Choose a voice:", list(voices.keys()))
voice_id = voices[selected_label]

# Voice stability slider
stability = st.slider("🎚️ Emotional Stability (lower = more expressive)", 0.0, 1.0, 0.5, 0.05)

# Generate button
if st.button("🎧 Generate Voice"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Synthesizing empathy..."):
            try:
                audio_stream = eleven_client.text_to_speech.convert(
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    text=text_input,
                    output_format="mp3_44100_128",
                    voice_settings={"stability": stability, "similarity_boost": 0.8},
                )

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    for chunk in audio_stream:
                        tmp.write(chunk)
                    tmp_path = tmp.name

                st.audio(tmp_path, format="audio/mp3")
                st.success(f"✅ Voice generated successfully — {selected_label}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
