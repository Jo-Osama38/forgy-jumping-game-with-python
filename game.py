import pygame
import sys
import os 
import random

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
wood_img = pygame.image.load(pathing("assets/wood.png"))

GRAVIGY = 1 
SCROLL_THEAM = 200
scroll = 0
bg_scroll = 0

def draw_bg(bg_scroll):
    screen.blit(bg_img,(0,0+bg_scroll))
    screen.blit(bg_img,(0,-600+bg_scroll))



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
        scroll = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.x > 0 :
            self.rect.x -= 7
            self.flip = True
        if key[pygame.K_d] and self.rect.x + self.width < SCREEN_WIDTH:
            self.rect.x += 7 
            self.flip = False

        self.vel_y += GRAVIGY 
        dy += self.vel_y


        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x ,self.rect.y + dy, self.width,self.hight):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0 :
                        self.rect.bottom = platform.rect.top
                        dy = 0 
                        self.vel_y = -20

        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0 
            self.vel_y = -20

        if self.rect.top <= SCROLL_THEAM:
            if self.vel_y < 0:
                scroll = -dy
        
        self.rect.y += dy + scroll

        return scroll


    def draw(self):
        screen.blit(pygame.transform.flip(self.img,self.flip,False) ,( self.rect.x -12 , self.rect.y -5) )


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(wood_img,(width,11))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll
       




jumpy = Player(SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)

platform_group = pygame.sprite.Group()
for p in range(70):
    p_w = random.randint(40,60)
    p_x = random.randint(0,SCREEN_WIDTH - p_w )
    p_y = p*random.randint(80,120) - 700
    platform = Platform(p_x,p_y,p_w)
    platform_group.add(platform)


while True:
    clock.tick(FPS)

    scroll = jumpy.move()
    bg_scroll += scroll
    if bg_scroll > 600:
        bg_scroll = 0 
    draw_bg(bg_scroll)
    pygame.draw.line(screen,(255,0,0),(0,SCROLL_THEAM),(SCREEN_WIDTH,SCROLL_THEAM))
    platform_group.draw(screen)
    platform_group.update(scroll)
    jumpy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
