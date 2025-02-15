import pyaudio
import wave
import requests
import os
import time
import openai
import pyttsx3


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Sarvam AI API details
SARVAM_API_URL = "https://api.sarvam.ai/speech-to-text-translate"
# API_KEY =   # 🔹 Replace with your API key
# OPENAI_API_KEY   # 🔹 Replace with your Open AI API key

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sample rate (standard)
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust for continuous speech
TEMP_WAV_FILE = "temp_audio.wav"


def record_audio(file_path, record_seconds=RECORD_SECONDS):
    """Records audio from the microphone and saves it as a WAV file."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("🎙️ Speak now... (Recording for", record_seconds, "seconds)")
    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))


def translate_speech(audio_file):
    """Sends recorded audio to Sarvam AI, retrieves translated text, and formats it for OpenAI API."""
    payload = {
        "model": "saaras:v1",
        "source_language": "te-IN",  # Telugu input
        "target_language": "en",  # English output
        "with_timesteps": "false"
    }

    try:
        with open(audio_file, "rb") as audio:
            files = [("file", ("audio.wav", audio, "audio/wav"))]
            headers = {"api-subscription-key": API_KEY}

            response = requests.post(SARVAM_API_URL, headers=headers, data=payload, files=files)
            print("\n🌐 API Response Status:", response.status_code)

            if response.status_code == 200:
                response_json = response.json()
                transcript = response_json.get("transcript", "Error: No text returned")
                print("📝 Transcript:", transcript)
                speak(f"You had asked: {transcript}")


                # Format prompt for OpenAI
                openai_prompt = f"Translate and answer: {transcript}"
                print("\n🔍 OpenAI Prompt:", openai_prompt)


                # Send to OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # or "gpt-3.5-turbo"
                    messages=[{"role": "user", "content": openai_prompt}],
                    api_key=OPENAI_API_KEY
                )

                openai_output = response["choices"][0]["message"]["content"]
                print("\n🤖 OpenAI Response:", openai_output)
                speak(f"Response and key points: {openai_output}")


                return openai_output
            else:
                print(f"❌ API Error: {response.text}")
                return None

    except FileNotFoundError:
        print("❌ Error: Audio file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to handle live speech translation."""
    while True:
        record_audio(TEMP_WAV_FILE)
        translated_text = translate_speech(TEMP_WAV_FILE)

        if translated_text:
            print("\n🔍 OpenAI Search Prompt:")
            print(translated_text)

        # Remove temp file
        os.remove(TEMP_WAV_FILE)

        # Delay before the next capture
        time.sleep(2)


if __name__ == "__main__":
    main()
