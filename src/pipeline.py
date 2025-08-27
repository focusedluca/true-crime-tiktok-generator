import argparse
import os
from script_generator import ScriptGenerator
from audio_generator import AudioGenerator
from video_generator import VideoGenerator

class TrueCrimePipeline:
    def __init__(self):
        self.script_gen = ScriptGenerator()
        self.audio_gen = AudioGenerator()
        self.video_gen = VideoGenerator()
    
    def process_episode(self, episode_number, skip_script=False, skip_audio=False, skip_video=False):
        print(f"\n{'='*50}")
        print(f"Processing Episode {episode_number}")
        print(f"{'='*50}\n")
        
        episode_dir = f"episodes/{episode_number}"
        if not os.path.exists(episode_dir):
            os.makedirs(episode_dir)
        
        # Generate script
        if not skip_script:
            try:
                self.script_gen.create_script_for_episode(episode_number)
            except Exception as e:
                print(f"Error generating script: {e}")
                return False
        
        # Generate audio
        if not skip_audio:
            try:
                self.audio_gen.create_audio(episode_number)
            except Exception as e:
                print(f"Error generating audio: {e}")
                return False
        
        # Generate video
        if not skip_video:
            try:
                self.video_gen.create_video(episode_number)
            except Exception as e:
                print(f"Error generating video: {e}")
                return False
        
        print(f"\n✅ Episode {episode_number} completed successfully!")
        return True
    
    def batch_process(self, start_episode, end_episode, **kwargs):
        successful = []
        failed = []
        
        for episode_num in range(start_episode, end_episode + 1):
            if self.process_episode(episode_num, **kwargs):
                successful.append(episode_num)
            else:
                failed.append(episode_num)
        
        print(f"\n{'='*50}")
        print("Batch Processing Complete")
        print(f"Successful: {len(successful)} episodes")
        print(f"Failed: {len(failed)} episodes")
        if failed:
            print(f"Failed episodes: {failed}")
        print(f"{'='*50}\n")

def main():
    parser = argparse.ArgumentParser(description="True Crime Video Generation Pipeline")
    parser.add_argument("--episode", type=int, help="Process a single episode")
    parser.add_argument("--batch", nargs=2, type=int, metavar=("START", "END"), 
                       help="Process episodes in batch (e.g., --batch 1 10)")
    parser.add_argument("--skip-script", action="store_true", help="Skip script generation")
    parser.add_argument("--skip-audio", action="store_true", help="Skip audio generation")
    parser.add_argument("--skip-video", action="store_true", help="Skip video generation")
    
    args = parser.parse_args()
    
    pipeline = TrueCrimePipeline()
    
    if args.episode:
        pipeline.process_episode(
            args.episode,
            skip_script=args.skip_script,
            skip_audio=args.skip_audio,
            skip_video=args.skip_video
        )
    elif args.batch:
        start, end = args.batch
        pipeline.batch_process(
            start, end,
            skip_script=args.skip_script,
            skip_audio=args.skip_audio,
            skip_video=args.skip_video
        )
    else:
        print("Please specify --episode or --batch option")
        parser.print_help()

if __name__ == "__main__":
    main()