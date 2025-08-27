# Quick Setup Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## 3. Add Media Files

### Background Music (`bg_music/`)
- Add 3-5 MP3 files of dark, atmospheric instrumental music
- Suggested sources: Pixabay, Freesound, Epidemic Sound
- Examples: ambient music, dark electronic, cinematic scores

### Background Videos (`bg_videos/`)
- Add 5-10 MP4 files of atmospheric footage
- Suggested content: rain, fog, urban scenes, textures, abstract visuals
- Suggested sources: Pexels, Pixabay, Videvo
- Any resolution works (system will resize)

## 4. Test the System
```bash
# Test with first example story
python src/pipeline.py --episode 1

# Or just generate the script to test
python src/pipeline.py --episode 1 --skip-audio --skip-video
```

## Common Issues

### "No background music files found"
- Add at least one MP3 file to `bg_music/`
- Check file extensions are lowercase `.mp3`

### "No background video files found"  
- Add at least one MP4 file to `bg_videos/`
- Check file extensions are lowercase `.mp4`

### "API key not found"
- Verify `.env` file exists and contains your API keys
- Check API key format and validity

### "FFmpeg not found"
- Install FFmpeg: `brew install ffmpeg` (Mac) or download from ffmpeg.org

## Ready to Go!
Once you have media files and API keys set up, you can:
- Process individual episodes: `python src/pipeline.py --episode X`  
- Batch process: `python src/pipeline.py --batch 1 5`
- Add your own stories to `data/stories/example_stories.txt`