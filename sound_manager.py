# sound_manager.py
import threading
import os
import pygame

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.sound_files = {
            'click': 'click.mp3',
            'finish': 'finish.mp3'
        }

    def play_sound(self, sound_name):
        sound_file = self.sound_files.get(sound_name)
        if sound_file and os.path.exists(sound_file):
            threading.Thread(target=self._play_sound_pygame, args=(sound_file,), daemon=True).start()
        else:
            print(f"Sound file '{sound_file}' not found.")

    def _play_sound_pygame(self, sound_file):
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            # Wait for the sound to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing sound: {e}")
