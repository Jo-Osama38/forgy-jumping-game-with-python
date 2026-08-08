import pygame
import sys
import os 

pygame.init()

clock = pygame.time.Clock()
FPS = 60

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

GRAVIGY = 1 

class Player():
    def __init__(self,x,y):
        self.img =pygame.transform.scale(player_img,(45,45)) 
        self.width = 25
        self.hight = 40
        self.rect = pygame.Rect(0,0,self.width,self.hight)
        self.rect.center = (x,y)
        self.flip = False
        self.vel_y = 0

    def move(self):

        dy =0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.x > 0 :
            self.rect.x -= 7
            self.flip = True
        if key[pygame.K_d] and self.rect.x + self.width < SCREEN_WIDTH:
            self.rect.x += 7 
            self.flip = False

        self.vel_y += GRAVIGY 
        dy += self.vel_y

        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0 
            self.vel_y = -20

        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.img,self.flip,False) ,( self.rect.x -12 , self.rect.y -5) )
        pygame.draw.rect(screen,(0,0,0),self.rect , 2)

jumpy = Player(SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)
        

while True:
    clock.tick(FPS)

    jumpy.move()
    screen.blit(bg_img,(0,0))
    jumpy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
