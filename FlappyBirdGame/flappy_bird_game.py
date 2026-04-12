import pygame
import os
#import nest
import time
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))) 
    ] 

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png"))) 
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png"))) 
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png"))) 

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird: 
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 
    ROT_VEL = 15 
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0 
        self.vel = 0 
        self.height = self.y
        self.img_count = 0 
        self.img = self.IMGS[self.img_count]

    def jump(self):
        self.vel = -8.5 
        self.tick_count = 0 
        self.height = self.y

    def move(self):
        self.tick_count += 1 
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if displacement >= 16: 
            displacement = 16 
        
        if displacement < 0: 
            displacement -= 2 

        self.y = self.y + displacement
        
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90: 
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
    
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) 
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img) 
    
class Pipe: 
    GAP = 200 
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False 
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL 
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird): 
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset) 
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point: 
            return True
        return False
    
class Base:
    VEL = 5 
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x_start = 0
        self.x_end = self.WIDTH

    def move(self): 
        self.x_start -= self.VEL
        self.x_end -= self.VEL

        if self.x_start + self.WIDTH < 0:
            self.x_start = self.x_end + self.WIDTH

        if self.x_end + self.WIDTH < 0:
            self.x_end = self.x_start + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x_start, self.y))
        win.blit(self.IMG, (self.x_end, self.y))

def draw_window(win, bird, pipes, base, score):
    win.blit(BACKGROUND_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

        text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def reset_game():
    main()

def main(): 
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False

        #to change
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()

        bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                reset_game()
                #pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe: 
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            reset_game()
            #pass

        base.move()

        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()

main()