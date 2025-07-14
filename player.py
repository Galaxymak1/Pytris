"""Class to manage the sound and music of the game"""

from config import BASE_VOLUME,MUSIC
from pygame import mixer
from pygame.mixer import Sound

class Player():
    def __init__(self):
        mixer.init()
        self.volume = BASE_VOLUME
        pass
    
    def play_sound(self,sound : Sound,volume = BASE_VOLUME):
        Sound(sound).play().set_volume(volume)
        pass

    def play_menu_music(self):
        mixer.music.load(MUSIC["menu"])
        mixer.music.set_volume(self.volume)  
        mixer.music.play(-1)

    def play_game_music(self):
        mixer.music.load(MUSIC["game"])
        mixer.music.set_volume(self.volume)  
        mixer.music.play(-1)

    def stop_music(self):
        mixer.music.stop()
        
