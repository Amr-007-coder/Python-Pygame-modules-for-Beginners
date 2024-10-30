#Example of how to use the 'modules.py' file

import pygame, sys
from modules import *

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FPS = 60
Clock = pygame.time.Clock()

font = pygame.font.SysFont("Comic Sans MS", 40)

button_img = pygame.image.load("images/button.png").convert_alpha()
active_button_img = pygame.image.load("images/active_button.png").convert_alpha()

button_actions = {
    "start": False,
    "y": False,
    "z": False,
}

progress = 0
def Handle():
    global progress

    displayText(screen, "Welcome", (SCREEN_WIDTH/2, SCREEN_HEIGHT/10), "black", font, True)
    displayImageButton(screen, button_actions, "start", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), (200, 88),
                       button_img, active_button_img, "black", font, True)
    
    #if start-button pressed -> progressbar will progress until start button is pressed again
    displayProgressBar(screen, (screen.get_width()/2 - 125, screen.get_height()*3/4), (250, 50), progress, "lightblue", "black")
    if button_actions["start"]:
        progress += 0.001

    displayFPS(screen, Clock, (0, 0), font, "black")

while __name__ == "__main__":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((177, 156, 217))
    Handle()
    pygame.display.update()
    Clock.tick(FPS)