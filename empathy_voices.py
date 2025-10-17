import tempfile
import streamlit as st
from elevenlabs import ElevenLabs

# Initialize ElevenLabs client (expects ELEVENLABS_API_KEY set in Streamlit secrets)
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

# --- Tone selection (use radio so selection persists across reruns) ---
st.write("### Choose a voice tone (overrides emotion detection):")
preferred_tone = st.radio("Tone", ("Auto (default)", "Calm", "Reassuring", "Nostalgic"))

# Map tone names to voice IDs
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
    if preferred_tone and preferred_tone != "Auto (default)":
        selected_voice = voice_map.get(preferred_tone.upper(), voice_map["CALM"])
    else:
        # Default to Calm if Auto or not selected
        selected_voice = voice_map["CALM"]

    # Optional: prepend style tags for emotion sliders (if supported by ElevenLabs)
    # If the ElevenLabs model doesn't support these tags, remove them.
    styled_text = f"<enthusiasm:{enthusiasm}><sadness:{sadness}>{text_input}"

    try:
        # Generate audio stream from ElevenLabs client
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=selected_voice,
            model_id="eleven_multilingual_v1",
            text=styled_text
        )

        # Combine streamed chunks into bytes
        audio_bytes = b"".join(audio_stream)

        # Play audio directly from bytes
        st.audio(audio_bytes, format="audio/mp3")
        st.success("✨ Voice generated successfully!")

    except Exception as e:
        st.error(f"Error generating audio: {e}")
