import streamlit as st
import tempfile
from elevenlabs import ElevenLabs

# Initialize ElevenLabs client
eleven_client = ElevenLabs()

# --- Streamlit UI ---
st.title("🎙️ Empathy Voices")
st.subheader("Because voices carry memories words alone can’t.")
st.write("Type something you wish you could hear again...")

text_input = st.text_area("Your message:", placeholder="Example: I miss hearing you read that poem...")

# --- Emotion buttons ---
st.write("### Choose a tone:")
col1, col2, col3 = st.columns(3)

tone = None
if col1.button("🕊️ Calm"):
    tone = "Calm"
if col2.button("💞 Reassuring"):
    tone = "Reassuring"
if col3.button("🌙 Nostalgic"):
    tone = "Nostalgic"

# Map tone to ElevenLabs voices
voice_map = {
    "Calm": "XB0fDUnXU5powFXDhCwa", #Charlotte
    "Reassuring": "9BWtsMINqrJLrRacOk9x",  #Aria
    "Nostalgic": "NOpBlnGInO9m6vDvFkFC" #Grandpa
}

# --- Generate voice ---
if tone and text_input:
    st.info(f"Generating a {tone.lower()} voice... please wait.")

    selected_voice = voice_map.get(tone, "Rachel")

    # Generate audio stream
    audio_stream = eleven_client.text_to_speech.convert(
        voice_id=selected_voice,
        model_id="eleven_multilingual_v2",
        text=text_input
    )

    # Combine all streamed chunks into a single bytes object
    audio_bytes = b"".join(audio_stream)

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    # Play the generated audio in Streamlit
    st.audio(temp_path, format="audio/mp3")
    st.success(f"✨ {tone} voice generated successfully!")

