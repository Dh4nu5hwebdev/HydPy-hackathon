# import openai use your open api
from twilio.rest import Client
from gtts import gTTS
import speech_recognition as sr
import os
import requests


# Secure credentials using environment variables
import dotenv
dotenv.load_dotenv()

# account_sid
# auth_token
client = Client(account_sid, auth_token)

# OPENAI_API_KEY = os.getenv()

# url
# API_KEY

payload = {
    'model': 'saarika:v1',
    'language_code': 'te-IN',  # Adjust language code if needed
    'with_timesteps': 'false'
}

audio_file_path = sr

# client = Client(account_sid, auth_token)
# openai.api_key = OPENAI_API_KEY

try:
    with open(audio_file_path, 'rb') as audio_file:
        files = [('file', ('sample_tenglish_audio.wav', audio_file, 'audio/wav'))]

        # Headers
        headers = {
            'api-subscription-key': API_KEY
        }

        # Send Request
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # Print Response
        print("STT Output:", response.text)

except FileNotFoundError:
    print("Error: Audio file not found. Please check the file path.")

except Exception as e:
    print(f"Error: {e}")



def make_call(phone_number, audio_url):
    call = client.calls.create(
      url="http://demo.twilio.com/docs/voice.xml",
      to="+916305438950",
      from_="+18284267836"
    )
    print(f"Call initiated to {phone_number}. Call SID: {call.sid}")


def speech_to_text(audio_url):
    """Convert speech to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()

    # Download and save the recording
    response = requests.get(audio_url)
    with open("recording.wav", "wb") as f:
        f.write(response.content)

    with sr.AudioFile("recording.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="te-IN")  # Telugu (India)
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError:
        print("Error with the speech recognition service.")
        return None


def text_to_speech(text, output_file="response.mp3"):
    """Convert text to speech using gTTS."""
    tts = gTTS(text=text, lang='te')  # Use 'te' for Telugu
    tts.save(output_file)
    print(f"TTS saved as {output_file}")

    # Play the audio
    if os.name == 'nt':  # Windows
        os.system(f"start {output_file}")
    elif os.name == 'posix':  # macOS/Linux
        os.system(f"mpg321 {output_file} &")


def openai_chat(prompt):
    """Generate a response using OpenAI's Chat API."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()


def main():
    phone_number = "+916305438950"  # Replace with actual phone number
    audio_url = "https://your-server.com/audio/recorded_audio.wav"  # Update with a real URL

    # Step 1: Make the call
    make_call(phone_number, audio_url)

    # Step 2: Simulate handling the recording (Twilio should send the recording URL)
    # recording_url = "https://your-server.com/audio/user_response.wav"  # Replace with the actual recording URL
    # text = speech_to_text(recording_url)
    #
    # if text:
    #     # Step 3: Generate a response using OpenAI
    #     response_text = openai_chat(text)
    #     print(f"AI Response: {response_text}")
    #
    #     # Step 4: Convert the response to speech
    #     text_to_speech(response_text)


if __name__ == '__main__':
    main()
