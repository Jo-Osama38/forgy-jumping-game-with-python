import pygame
import sys
import os 

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def pathing(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("FORGGY JUPMING GAME")

bg_img = pygame.image.load(pathing("assets/bg.png"))

while True:

    screen.blit(bg_img,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
