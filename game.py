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


bg_img = pygame.image.load(pathing("assets/bg.jpg"))
player_img= pygame.image.load(pathing("assets/jump.png"))
wood_img = pygame.image.load(pathing("assets/platform.png"))
bg_img = pygame.transform.scale(bg_img,(400,600)) 

GRAVIGY = 1 
SCROLL_THEAM = 200
scroll = 0
bg_scroll = 0
MAX_PLATFORM = 10
game_over = False
score = 0

font_small = pygame.font.SysFont("Lucida Sans",20)
font_big = pygame.font.SysFont("Lucida Sans",26)

def draw_text (text , font,color, x,y):
    img = font.render(text ,True,color)
    screen.blit(img,(x,y))



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
        self.width = wood_img.get_width()
        self.height = wood_img.get_height()
        self.image = pygame.transform.scale(wood_img,(width,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
       




jumpy = Player(SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)

platform_group = pygame.sprite.Group()
platform = Platform(SCREEN_WIDTH // 2 -35 ,SCREEN_HEIGHT -50 , 70 )
platform_group.add(platform)


while True:
    clock.tick(FPS)

    if not game_over:
        scroll = jumpy.move()
        bg_scroll += scroll
        if bg_scroll > 600:
            bg_scroll = 0 
        draw_bg(bg_scroll)

        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(50,70)
            p_x = random.randint(0 , SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80,120)
            platform = Platform(p_x , p_y , p_w)
            platform_group.add(platform)
        platform_group.draw(screen)
        platform_group.update(scroll)
        jumpy.draw()

        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        draw_text("GAME OVER",font_big,(255,255,0),130,200)
        draw_text("SCORE: "+str(score),font_big,(255,0,255),130,250)
        draw_text("PRESS SPACE TO PLAY AGAIN",font_big,(0,255,255),40,300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            scroll = 0

            jumpy.rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)

            platform_group.empty()

            platform = Platform(SCREEN_WIDTH // 2 -35 ,SCREEN_HEIGHT -50 , 70 )
            platform_group.add(platform)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
