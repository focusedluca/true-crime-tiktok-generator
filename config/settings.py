import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "TxGEqnHWrfWFTfGW9XjX")

# OpenAI Settings
OPENAI_MODEL = "gpt-4o"
SCRIPT_TEMPERATURE = 1.0

# ElevenLabs Settings
ELEVENLABS_MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": False
}

# Video Settings
VIDEO_FPS = int(os.getenv("VIDEO_FPS", 64))
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", 1620))  # 1080 * 1.5
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", 2880))  # 1920 * 1.5
BG_MUSIC_VOLUME = float(os.getenv("BG_MUSIC_VOLUME", 0.1))
AUDIO_SPEED_FACTOR = float(os.getenv("AUDIO_SPEED_FACTOR", 1.0))
EXTRA_DURATION = 5  # Extra seconds after script ends

# Subtitle Settings
SUBTITLE_CONFIG = {
    'fontsize': 110,
    'color': 'white',
    'font': 'Arial-Bold',
    'stroke_color': 'black',
    'stroke_width': 2,
    'position_y_offset': 862.5  # 575 * 1.5
}

# Whisper Settings
WHISPER_MODEL = "base"
WHISPER_DEVICE = "cpu"

# Directory Paths
BG_MUSIC_DIR = "bg_music"
BG_VIDEOS_DIR = "bg_videos"
EPISODES_DIR = "episodes"
DATA_DIR = "data"
PROMPTS_DIR = "data/prompts"
STORIES_DIR = "data/stories"