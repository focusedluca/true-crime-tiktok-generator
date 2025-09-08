# True Crime TikTok Generator

An automated pipeline for generating short-form true crime videos with AI-generated scripts, narration, and subtitles. Perfect for creating engaging TikTok content, YouTube Shorts, and Instagram Reels.

## Features

- **AI Script Generation**: Converts brief crime story descriptions into engaging English narratives using OpenAI's GPT-4
- **Professional Narration**: Text-to-speech conversion using ElevenLabs' realistic voice synthesis
- **Automated Video Production**: Combines narration with background videos and music
- **Dynamic Subtitles**: Automatic transcription and word-level subtitle generation using Whisper
- **Batch Processing**: Process multiple episodes efficiently with customizable pipeline
- **Configurable Settings**: Easily adjustable video parameters, voice settings, and more

## Project Structure

```
true-crime-tiktok-generator/
│
├── src/                     # Source code
│   ├── script_generator.py  # AI script generation
│   ├── audio_generator.py   # Text-to-speech conversion
│   ├── video_generator.py   # Video assembly and subtitles
│   └── pipeline.py          # Main processing pipeline
│
├── config/                  # Configuration files
│   └── settings.py          # Application settings
│
├── data/                    # Data files
│   ├── prompts/            # AI prompts
│   │   └── script_system_prompt.txt
│   └── stories/            # Crime story descriptions
│       └── 100_stories.txt
│
├── bg_music/               # Background music files
├── bg_videos/              # Background video clips
├── episodes/               # Generated episode content
│   └── {episode_number}/
│       ├── script.txt      # Generated narrative
│       ├── audio.mp3       # Narration audio
│       ├── video.mp4       # Final video
│       ├── video_with_subs.mp4  # Video with subtitles
│       └── video_info.txt  # Production metadata
│
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- OpenAI API key
- ElevenLabs API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/true-crime-tiktok-generator.git
cd true-crime-tiktok-generator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `ELEVENLABS_VOICE_ID`: Voice ID for narration (default: Josh)

4. Add your media assets:
- **Background Music**: Add MP3 files to `bg_music/` (see `bg_music/README.md` for details)
- **Background Videos**: Add MP4 files to `bg_videos/` (see `bg_videos/README.md` for requirements)  
- **Stories**: Add your story files to `data/stories/` (see format section below)

**Note**: Your personal media files and episodes won't be tracked by git due to `.gitignore` settings.

## Repository Structure

### What's Included in Git:
- ✅ Source code (`src/`)
- ✅ Configuration templates (`.env.example`, `config/`)
- ✅ Documentation (`README.md`, setup guides)
- ✅ Example story file (`data/stories/example_stories.txt`)
- ✅ One example episode (`episodes/example/`)

### What's Excluded from Git (.gitignored):
- ❌ Your personal media files (`bg_music/*.mp3`, `bg_videos/*.mp4`)
- ❌ Your story files (`data/stories/100_stories.txt`, etc.)
- ❌ Generated episodes (`episodes/1/`, `episodes/2/`, etc.)
- ❌ API keys and environment files (`.env`)

This keeps your personal content private while sharing the working code.

## Usage

### Quick Start

1. **Test with example data**:
```bash
# Process episode 1 using example stories
python src/pipeline.py --episode 1
```

2. **Process multiple episodes**:
```bash
# Process episodes 1 through 5
python src/pipeline.py --batch 1 5
```

**Note**: You need to add your own background music and video files first (see installation step 4).

## Media Setup Guide

### Background Music
1. Download royalty-free instrumental music suitable for true crime content
2. Save as MP3 files in the `bg_music/` directory
3. Recommended: Dark, atmospheric, suspenseful instrumental tracks
4. The system will randomly select and loop music to match video length

### Background Videos  
1. Download stock video footage (MP4 format)
2. Save in the `bg_videos/` directory  
3. Recommended: Abstract, atmospheric footage (fog, rain, urban scenes, textures)
4. The system will randomly combine clips and resize to vertical format

### Story Content
1. Use the provided `data/stories/example_stories.txt` as a starting point
2. Add your own stories following the same format
3. Keep descriptions brief (1-2 sentences)
4. Focus on well-known, public domain cases

### Selective Processing

Skip certain steps in the pipeline:
```bash
# Generate only script and audio (skip video)
python src/pipeline.py --episode 5 --skip-video

# Generate only video (assuming script and audio exist)
python src/pipeline.py --episode 5 --skip-script --skip-audio
```

### Python API

```python
from src.pipeline import TrueCrimePipeline

# Initialize pipeline
pipeline = TrueCrimePipeline()

# Process single episode
pipeline.process_episode(episode_number=1)

# Batch process with options
pipeline.batch_process(
    start_episode=1,
    end_episode=10,
    skip_script=False,
    skip_audio=False,
    skip_video=False
)
```

## Configuration

### Video Settings

Edit `config/settings.py` or set environment variables:

- `VIDEO_FPS`: Frame rate (default: 64)
- `VIDEO_WIDTH`: Video width in pixels (default: 1620)
- `VIDEO_HEIGHT`: Video height in pixels (default: 2880)
- `BG_MUSIC_VOLUME`: Background music volume 0-1 (default: 0.1)
- `AUDIO_SPEED_FACTOR`: Narration speed multiplier (default: 1.0)

### Voice Settings

Configure ElevenLabs voice parameters in `config/settings.py`:

```python
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": False
}
```

### Subtitle Appearance

Customize subtitle styling in `config/settings.py`:

```python
SUBTITLE_CONFIG = {
    'fontsize': 110,
    'color': 'white',
    'font': 'Arial-Bold',
    'stroke_color': 'black',
    'stroke_width': 2
}
```

## Story File Format

The system reads stories from text files in `data/stories/`. Here's the exact format required:

### Format Requirements:
```
{number}. **{Title}**:
   {Description in 1-2 sentences}

{number}. **{Next Title}**:
   {Next description}
```

### Important Details:
- **Number Format**: `{number}.` followed by a space
- **Title Format**: `**{Title}**:` (bold markdown with colon)
- **Indentation**: Description must be indented with 3 spaces
- **Separation**: Double line break between stories
- **Language**: The system works with any language input (German, English, etc.)

### Example:
```
1. **Der Zodiac-Killer**:
   Ein Serienmörder terrorisierte San Francisco in den 1960er und 1970er Jahren.

2. **The Black Dahlia Murder**:
   Elizabeth Short was found brutally murdered in Los Angeles in 1947.
```

### File Configuration:
- Default file: `data/stories/100_stories.txt`  
- You can specify different files in the code: `stories_file="path/to/your/file.txt"`
- Create multiple story files for different categories or languages

## API Rate Limits

Be mindful of API usage:
- OpenAI: Check your plan's rate limits
- ElevenLabs: Monthly character limits apply
- Consider implementing delays for batch processing

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Ensure FFmpeg is installed and in your PATH
2. **API errors**: Verify your API keys are correct and have sufficient credits
3. **Memory issues**: Large video files may require significant RAM
4. **Missing dependencies**: Run `pip install -r requirements.txt`

### Performance Tips

- Use smaller/shorter background videos to reduce processing time
- Adjust `VIDEO_FPS` to balance quality and file size
- Process episodes in smaller batches to avoid rate limits
- Consider using GPU acceleration for Whisper transcription

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- ElevenLabs for voice synthesis
- OpenAI Whisper for transcription
- MoviePy for video processing

## Disclaimer

This project is intended for educational purposes. When creating content about true crime:
- Be respectful to victims and their families
- Verify facts before publishing
- Follow platform guidelines for sensitive content
- Consider the ethical implications of true crime content

## Contact

For questions or support, please open an issue on GitHub.