import pygame
import random

class Enemy (pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH ,y ,imgList,score):
        pygame.sprite.Sprite.__init__(self)
        if len(imgList) == 2 and score < 2500:
            self.direction = random.choice([-2,2])
        elif len(imgList) == 2 and score > 5000:
            self.direction = random.choice([-4,4])
        elif len(imgList) == 4 :
            self.direction = random.choice([-3,3])


        if self.direction < 0:
            self.flip = True
        else: self.flip = False


        self.animation_list = imgList
        self.fram_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.fram_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        
        if self.direction >0:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH

    def update(self,SCREEN_WIDTH,scroll):

        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.fram_index]
        self.image = pygame.transform.flip(self.image , self.flip , False)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.fram_index += 1 
            self.update_time = pygame.time.get_ticks()
        if self.fram_index >= len(self.animation_list):
            self.fram_index = 0



        self.rect.x += self.direction
        self.rect.y += scroll

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

