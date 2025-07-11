# CLI Tetris written in Python

import pygame

from game import Game


def play_music(path: str):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play(-1)                       

def game():
    game = Game()
    game.state.is_running =  True
    game.main_loop()
              
def main():
    game()

        

if __name__ == "__main__":
    main()