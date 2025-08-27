import os
import random
import tempfile
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeAudioClip,
    concatenate_videoclips, TextClip, CompositeVideoClip
)
from pydub import AudioSegment
import whisper_timestamped as whisper

class VideoGenerator:
    def __init__(self):
        self.bg_music_folder = 'bg_music'
        self.bg_videos_folder = 'bg_videos'
        self.output_width = int(1080 * 1.5)
        self.output_height = int(1920 * 1.5)
        self.fps = 64
        self.subtitle_config = {
            'fontsize': 110,
            'color': 'white',
            'font': 'Arial-Bold',
            'stroke_color': 'black',
            'stroke_width': 2,
            'position_y_offset': 575 * 1.5
        }
    
    def create_video(self, episode_number, speed_factor=1.0, bg_music_volume=0.1, extra_duration=5):
        episode_folder = f'episodes/{episode_number}'
        script_audio_path = os.path.join(episode_folder, 'audio.mp3')
        output_video_path = os.path.join(episode_folder, 'video.mp4')
        video_with_subs_path = os.path.join(episode_folder, 'video_with_subs.mp4')
        video_info_path = os.path.join(episode_folder, 'video_info.txt')
        
        if not os.path.exists(script_audio_path):
            raise FileNotFoundError(f"Audio for episode {episode_number} not found at {script_audio_path}")
        
        print(f"Creating video for episode {episode_number}...")
        
        # Process audio
        script_audio_clip = self._process_audio(script_audio_path, speed_factor, episode_folder)
        script_duration = script_audio_clip.duration
        total_duration = script_duration + extra_duration
        
        # Create background music
        bg_music_file, bg_music_audio = self._create_background_music(total_duration, bg_music_volume)
        
        # Combine audio tracks
        combined_audio = CompositeAudioClip([
            bg_music_audio,
            script_audio_clip.set_end(script_duration)
        ])
        
        # Create background video
        bg_video_clip, videos_used = self._create_background_video(total_duration)
        
        # Combine video and audio
        final_video = bg_video_clip.set_audio(combined_audio)
        final_video.write_videofile(output_video_path, fps=self.fps, audio_codec='aac')
        print(f"Video saved at {output_video_path}")
        
        # Add subtitles
        self._add_subtitles_to_video(output_video_path, video_with_subs_path)
        
        # Save video information
        self._save_video_info(video_info_path, bg_music_file, videos_used)
        
        return output_video_path, video_with_subs_path
    
    def _process_audio(self, audio_path, speed_factor, episode_folder):
        if speed_factor == 1.0:
            return AudioFileClip(audio_path)
        
        script_audio = AudioSegment.from_file(audio_path)
        
        def change_speed(sound, speed=1.0):
            sound_with_altered_frame_rate = sound._spawn(
                sound.raw_data,
                overrides={"frame_rate": int(sound.frame_rate * speed)},
            )
            return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
        
        script_audio = change_speed(script_audio, speed_factor)
        temp_audio_path = os.path.join(episode_folder, 'script_temp.mp3')
        script_audio.export(temp_audio_path, format='mp3')
        
        return AudioFileClip(temp_audio_path)
    
    def _create_background_music(self, duration, volume):
        bg_music_files = [
            f for f in os.listdir(self.bg_music_folder)
            if os.path.isfile(os.path.join(self.bg_music_folder, f))
        ]
        
        if not bg_music_files:
            raise FileNotFoundError(f"No background music files found in {self.bg_music_folder}")
        
        bg_music_file = random.choice(bg_music_files)
        bg_music_path = os.path.join(self.bg_music_folder, bg_music_file)
        
        bg_music_audio = AudioFileClip(bg_music_path)
        bg_music_audio = bg_music_audio.volumex(volume)
        bg_music_audio = bg_music_audio.fx(AudioFileClip.audio_loop, duration=duration)
        bg_music_audio = bg_music_audio.set_duration(duration)
        
        return bg_music_file, bg_music_audio
    
    def _create_background_video(self, duration):
        bg_video_files = [
            f for f in os.listdir(self.bg_videos_folder)
            if os.path.isfile(os.path.join(self.bg_videos_folder, f))
        ]
        
        if not bg_video_files:
            raise FileNotFoundError(f"No background video files found in {self.bg_videos_folder}")
        
        bg_video_clips = []
        current_duration = 0
        videos_used = []
        
        while current_duration < duration:
            video_file = random.choice(bg_video_files)
            video_path = os.path.join(self.bg_videos_folder, video_file)
            clip = VideoFileClip(video_path, audio=False)
            clip_duration = clip.duration
            
            if current_duration + clip_duration > duration:
                remaining_duration = duration - current_duration
                clip = clip.subclip(0, remaining_duration)
                clip_duration = remaining_duration
            
            bg_video_clips.append(clip)
            videos_used.append({
                'file': video_file,
                'start_time': current_duration,
                'duration': clip_duration
            })
            current_duration += clip_duration
        
        bg_video_clip = concatenate_videoclips(bg_video_clips)
        bg_video_clip = bg_video_clip.resize((self.output_width, self.output_height))
        
        return bg_video_clip, videos_used
    
    def _add_subtitles_to_video(self, video_path, output_path):
        print("Transcribing audio and generating subtitles...")
        
        # Extract and transcribe audio
        video = VideoFileClip(video_path)
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
            video.audio.write_audiofile(audio_file.name, codec='pcm_s16le', logger=None)
            audio_path = audio_file.name
        
        # Transcribe with Whisper
        model = whisper.load_model("base", device="cpu")
        result = whisper.transcribe(model, audio_path)
        
        # Extract subtitles
        subtitles = []
        for segment in result['segments']:
            for word_info in segment['words']:
                subtitles.append((word_info['start'], word_info['end'], word_info['text']))
        
        # Add subtitles to video
        subtitle_clips = []
        for start_time, end_time, text in subtitles:
            txt_clip = TextClip(
                text,
                fontsize=self.subtitle_config['fontsize'],
                color=self.subtitle_config['color'],
                font=self.subtitle_config['font'],
                stroke_color=self.subtitle_config['stroke_color'],
                stroke_width=self.subtitle_config['stroke_width']
            )
            txt_clip = txt_clip.set_position(
                ('center', video.h - self.subtitle_config['position_y_offset'])
            ).set_start(start_time).set_end(end_time)
            subtitle_clips.append(txt_clip)
        
        video_with_subs = CompositeVideoClip([video, *subtitle_clips])
        video_with_subs.audio = video.audio
        video_with_subs.write_videofile(output_path, codec="libx264", fps=self.fps, audio_codec='aac')
        
        print(f"Video with subtitles saved at {output_path}")
        
        # Clean up temporary file
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    def _save_video_info(self, info_path, bg_music_file, videos_used):
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(f"Background Music File: {bg_music_file}\n")
            f.write("Background Videos Used:\n")
            for video in videos_used:
                f.write(
                    f"  - File: {video['file']}, "
                    f"Start Time: {video['start_time']:.2f}s, "
                    f"Duration: {video['duration']:.2f}s\n"
                )