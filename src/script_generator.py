from openai import OpenAI
import os
from dotenv import load_dotenv

class ScriptGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self):
        prompt_path = "data/prompts/script_system_prompt.txt"
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    def get_story_info(self, story_number, stories_file="data/stories/100_stories.txt"):
        with open(stories_file, "r", encoding="utf-8") as f:
            content = f.read()
        stories = content.strip().split('\n\n')
        if 1 <= story_number <= len(stories):
            return stories[story_number - 1]
        else:
            raise ValueError(f"Story number {story_number} not found in {stories_file}")
    
    def generate_script(self, story_info, temperature=1):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": story_info}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    def create_script_for_episode(self, episode_number):
        print(f"Generating script for episode {episode_number}...")
        
        story_info = self.get_story_info(episode_number)
        script = self.generate_script(story_info)
        
        episode_dir = f"episodes/{episode_number}"
        if not os.path.exists(episode_dir):
            os.makedirs(episode_dir)
        
        with open(f"{episode_dir}/script.txt", "w", encoding="utf-8") as f:
            f.write(script)
        
        print(f"Script for episode {episode_number} generated successfully.")
        return script