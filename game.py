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
player_img= pygame.image.load(pathing("assets/jump.png"))

class Player():
    def __init__(self,x,y):
        self.img =pygame.transform.scale(player_img,(45,45)) 
        self.width = 25
        self.hight = 40
        self.rect = pygame.Rect(0,0,self.width,self.hight)
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.img ,( self.rect.x -12 , self.rect.y -5) )
        pygame.draw.rect(screen,(0,0,0),self.rect , 2)

jumpy = Player(SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)
        

while True:

    screen.blit(bg_img,(0,0))
    jumpy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
