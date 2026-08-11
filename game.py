import pygame
import sys
import os 
import random
from enemy import Enemy


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
bird1_img = pygame.image.load(pathing("assets/bird1.png"))
bird1_img = pygame.transform.scale(bird1_img,(45,40))
bird2_img = pygame.image.load(pathing("assets/bird2.png"))
bird2_img = pygame.transform.scale(bird2_img,(45,40))
imgList = [bird1_img,bird2_img]

GRAVIGY = 1 
SCROLL_THEAM = 200
scroll = 0
bg_scroll = 0
MAX_PLATFORM = 10
game_over = False
score = 0
fade_counter = 0 

if os.path.exists("score.txt"):
    with open("score.txt" ,"r") as file:
        high_score = int(file.read())
else:
    high_score = 0 

font_small = pygame.font.SysFont("comicsans",20)
font_big = pygame.font.SysFont("comicsans",30)
game_over_font = pygame.font.SysFont("comicsans",60)

def draw_text (text , font,color, x,y):
    img = font.render(text ,True,color)
    screen.blit(img,(x-img.get_width() // 2,y))



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
    def __init__(self,x,y,width,moving):
        pygame.sprite.Sprite.__init__(self)
        self.width = wood_img.get_width()
        self.height = wood_img.get_height()
        self.image = pygame.transform.scale(wood_img,(width,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.speed_moveing = random.randint(1,2)
        self.move_counter = random.randint(0,50)
        self.move_direction = random.choice([-self.speed_moveing,self.speed_moveing])


    def update(self, scroll):
        if self.moving :
            self.move_counter += 1 
            self.rect.x += self.move_direction
        if self.move_counter >= 100  or self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
             self.move_direction *= -1 
             self.move_counter = 0




        self.rect.y += scroll

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
       




jumpy = Player(SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)

platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


platform = Platform(SCREEN_WIDTH // 2 -35 ,SCREEN_HEIGHT -50 , 70 ,False)
platform_group.add(platform)


while True:
    clock.tick(FPS)

    if not game_over:
        scroll = jumpy.move()
        bg_scroll += scroll
        if bg_scroll > 600:
            bg_scroll = 0 
        draw_bg(bg_scroll)

        if scroll > 0 :
            score += scroll

        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(50,70)
            p_x = random.randint(0 , SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80,120)
            if score > 500:
                p_moving = random.choice([False,True,False])
            else:p_moving = False

            platform = Platform(p_x , p_y , p_w , p_moving)
            platform_group.add(platform)
        if len(enemy_group) == 0:
                    enemy = Enemy(SCREEN_WIDTH,100,bird1_img,imgList)
                    enemy_group.add(enemy)

        enemy_group.update(SCREEN_WIDTH,scroll)
        
        platform_group.draw(screen)
        platform_group.update(scroll)
        enemy_group.draw(screen)
        jumpy.draw()

        draw_text("SCORE: "+str(score),font_small, (255,255,255),80,20)

        pygame.draw.line(screen,(255,0,0),(0,score-high_score+SCROLL_THEAM),(SCREEN_WIDTH,score-high_score+SCROLL_THEAM),3)
        draw_text("HIGH SCORE" ,font_small,(255,0,0),330,score-high_score+SCROLL_THEAM)

        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            pygame.draw.rect(screen ,(0,0,0), (0,0,fade_counter,SCREEN_HEIGHT/4))
            pygame.draw.rect(screen ,(0,0,0), (SCREEN_WIDTH - fade_counter,SCREEN_HEIGHT//4 , SCREEN_WIDTH, SCREEN_HEIGHT /4))
            pygame.draw.rect(screen ,(0,0,0), (0,SCREEN_HEIGHT//2,fade_counter,SCREEN_HEIGHT/4))
            pygame.draw.rect(screen ,(0,0,0), (SCREEN_WIDTH - fade_counter,SCREEN_HEIGHT- SCREEN_HEIGHT//4 , SCREEN_WIDTH, SCREEN_HEIGHT /4))
        else:

            if score > high_score:
                high_score = score
                with open("score.txt","w") as file:
                    file.write(str(high_score))
                 
            
            draw_text("GAME OVER",game_over_font,(200 ,0,200),200,150)
            draw_text("HIGH SCORE: "+str(high_score),font_big,(0,150,150),200,270)
            draw_text("SCORE: "+str(score),font_big,(0,150,150),200,320)
            draw_text("PRESS SPACE TO PLAY AGAIN",font_small,(0,155,155),200,400)

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0

                jumpy.rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT - 150)

                platform_group.empty()
                enemy_group.empty()

                platform = Platform(SCREEN_WIDTH // 2 -35 ,SCREEN_HEIGHT -50 , 70,False )
                platform_group.add(platform)
            


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open("score.txt","w") as file:
                    file.write(str(high_score))
            quit()

    pygame.display.update()
