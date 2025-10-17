from elevenlabs import ElevenLabs
import streamlit as st

eleven_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])



# --- Streamlit UI ---
st.title("🎙️ Empathy Voices")
st.subheader("Because voices carry memories words alone can’t.")
st.write("Type something you wish you could hear again...")

# User text input
text_input = st.text_area(
    "Your message:", 
    placeholder="Example: I miss hearing you read that poem..."
)

# --- Tone selection ---
st.write("### Choose a voice tone (overrides emotion detection):")
col1, col2, col3 = st.columns(3)

preferred_tone = None
if col1.button("🕊️ Calm"):
    preferred_tone = "Calm"
if col2.button("💞 Reassuring"):
    preferred_tone = "Reassuring"
if col3.button("🌙 Nostalgic"):
    preferred_tone = "Nostalgic"

# Map tone names to abs voice IDs
voice_map = {
    "CALM": "XB0fDUnXU5powFXDhCwa",       # Charlotte
    "REASSURING": "9BWtsMINqrJLrRacOk9x", # Aria
    "NOSTALGIC": "NOpBlnGInO9m6vDvFkFC"   # Grandpa
}

# --- Optional: Emotion intensity sliders ---
st.write("### Optional: Adjust subtle emotional intensity")
enthusiasm = st.slider("Enthusiasm", 0.0, 1.0, 0.5)
sadness = st.slider("Sadness", 0.0, 1.0, 0.0)

# --- Generate voice ---
if text_input:
    st.info("Generating voice... please wait.")

    # Determine which voice to use
    if preferred_tone:
        selected_voice = voice_map.get(preferred_tone.upper(), "XB0fDUnXU5powFXDhCwa")
    else:
        # If no tone selected, default to Calm
        selected_voice = voice_map["CALM"]

    # Optional: prepend style tags for emotion sliders (if supported by ElevenLabs)
    styled_text = f"<enthusiasm:{enthusiasm}><sadness:{sadness}>{text_input}"

    # Generate audio stream
    audio_stream = eleven_client.text_to_speech.convert(
        voice_id=selected_voice,
        model_id="eleven_multilingual_v2",
        text=styled_text
    )

    # Combine streamed chunks
    audio_bytes = b"".join(audio_stream)

    # Save temporary mp3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    # Play audio in Streamlit
    st.audio(temp_path, format="audio/mp3")
    st.success(f"✨ Voice generated successfully!")
