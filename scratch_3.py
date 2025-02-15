import requests
import json
import os

# 🔹 Replace with your API key
# SARVAM_API_KEY

# 🔹 Sarvam AI API Endpoint
# SARVAM_API_URL


OUTPUT_DIR = r"C:\Users\Dhanush\Desktop\Health_Polocy\Summ"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)  # Creates the directory if it doesn’t exist

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "summary.txt")


# 🔹 Function to transcribe audio using Sarvam AI
def transcribe_audio(audio_path):
    """Sends an audio file to Sarvam AI for transcription."""

    payload = {
        "model": "saaras:v1",
        "source_language": "te-IN",  # Telugu + English (Code-Switching)
        "target_language": "en",  # English output
        "with_timesteps": "false"
    }

    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(audio_path, "rb") as audio:
        files = [("file", ("C:\\Users\\Dhanush\\Downloads\\sample_tenglish_audio.wav", audio, "audio/wav"))]

        response = requests.post(SARVAM_API_URL, headers=headers, data=payload, files=files)

        if response.status_code == 200:
            result = response.json()
            transcript = result.get("transcript", "").strip()

            if not transcript:
                print("⚠ Warning: No text returned from API.")
                return None

            print("\n📝 Transcription:\n", transcript)
            return transcript
        else:
            print(f"❌ API Error: {response.text}")
            return None


# 🔹 Function to summarize text
def summarize_text(text):
    """Creates a summarized version of the transcribed text."""

    # Simulated summarization (replace with an AI model if needed)
    if len(text) < 50:
        return text  # No need to summarize very short text
    else:
        sentences = text.split(". ")
        summary = ". ".join(sentences[:3])  # Take the first 3 sentences
        return summary + "..."


# 🔹 Function to save summary as a text file
def save_summary(summary):
    """Saves the summarized text to a specified file path."""

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(summary)
        print(f"\n✅ Summary saved to {OUTPUT_FILE}")  # Full path confirmation
    except Exception as e:
        print(f"❌ Error saving file: {e}")


# 🔹 Main execution
def main():
    """Main function to process an audio file, transcribe, summarize, and save."""

    audio_file = "C:\\Users\\Dhanush\\Downloads\\sample_tenglish_audio.wav"  # Replace with your audio file path

    print("🔹 Transcribing audio...")
    transcribed_text = transcribe_audio(audio_file)

    if transcribed_text:
        print("\n🔹 Summarizing text...")
        summary = summarize_text(transcribed_text)
        print("\n📌 Summary:\n", summary)

        save_summary(summary)
    else:
        print("⚠ No valid transcription found. Summary not saved.")


if __name__ == "__main__":
    main()
