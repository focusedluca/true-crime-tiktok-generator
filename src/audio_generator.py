import requests
import os
from dotenv import load_dotenv

class AudioGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "TxGEqnHWrfWFTfGW9XjX")  # Default: Josh (Legacy)
        self.model_id = "eleven_multilingual_v2"
    
    def create_audio(self, episode_number):
        script_path = f"episodes/{episode_number}/script.txt"
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script for episode {episode_number} not found at {script_path}")
        
        with open(script_path, 'r', encoding='utf-8') as f:
            speech_text = f.read()
        
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": speech_text,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": False
            }
        }
        
        print(f"Generating audio for episode {episode_number}...")
        response = requests.post(tts_url, headers=headers, json=data, stream=False)
        
        if response.ok:
            audio_path = f"episodes/{episode_number}/audio.mp3"
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            print(f"Audio for episode {episode_number} saved at {audio_path}")
            return audio_path
        else:
            raise Exception(f"Failed to generate audio: Status {response.status_code}, Response: {response.text}")