import pygame
import time
#import math

WHITE =     (255, 255, 255)
BLUE =      (0, 0, 255)
GREEN =     (0, 255, 0)
YELLOW = (255, 255, 0)
RED =       (255, 0, 0)
BLACK = (0, 0, 0)
TEXTCOLOR = (  0,   0,  0)

HEIGHT = 640
WIDTH = 1280

FPS = 60

pygame.init()
clock = pygame.time.Clock()

# music
bgm = pygame.mixer.music.load("resources\\music\\This_is_the_end.mp3")
#pygame.mixer.music.play(-1)

# sounds
resume_sound = pygame.mixer.Sound("resources\\sound_effects\\resume.wav")
button_hover_sound = pygame.mixer.Sound("resources\\sound_effects\\button_hover.wav")

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        #button_hover_sound.play()

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText , WHITE)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def pause():
    global paused
    pygame.mixer.music.pause()
    paused = True 
    while paused:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    resume()

        largeText =pygame.font.Font("resources\\fonts\\ZOMBIES_REBORN.ttf", 150)
        TextSurf, TextRect = text_objects("Paused", largeText, RED)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button("Continue", 150, 450 , 100 ,50,GREEN,BLUE,resume)
        button("Quit",550,450,100,50,RED,YELLOW,pygame.quit)

        pygame.display.update()

def resume():
    global paused
    #resume_sound.play()
    paused = False
    pygame.mixer.music.play(-1)


def game_intro():
    global intro
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        largeText = pygame.font.Font("resources\\fonts\\ZOMBIES_REBORN.ttf",200)
        TextSurf, TextRect = text_objects("TEST1", largeText, RED)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,GREEN,BLUE,game_loop)
        button("Quit",550,450,100,50,RED,YELLOW,pygame.quit)

        pygame.display.update()
        clock.tick(15)

    

skull_cage_bck = pygame.image.load("resources\\backgrounds\\skull_cage.jpg")
skull_cage_dark_bck = pygame.image.load("resources\\backgrounds\\skull_cage_dark.jpg")
skull_passage_bck = pygame.image.load("resources\\backgrounds\\skull_passage.jpg")
fallen_pillar_bck = pygame.image.load("resources\\backgrounds\\fallen_pillar.jpg")
ruined_passage_bck = pygame.image.load("resources\\backgrounds\\ruined_passage.jpg")
bloody_sewage_bck = pygame.image.load("resources\\backgrounds\\bloody_sewage.jpg")
ruined_passage_dark_bck = pygame.image.load("resources\\backgrounds\\ruined_passage_dark.jpg")
prayer_room_bck = pygame.image.load("resources\\backgrounds\\prayer_room.jpg")
ship_wreck_bck = pygame.image.load("resources\\backgrounds\\ship_wreck.jpg")
violet_bck = pygame.image.load("resources\\backgrounds\\violet.jpg")
graveyard_bck = pygame.image.load("resources\\backgrounds\\graveyard.jpg")
clean_passage_back = pygame.image.load("resources\\backgrounds\\clean_passage.jpg")

bck_list = [skull_cage_bck,skull_cage_dark_bck,skull_passage_bck,fallen_pillar_bck,ruined_passage_bck,bloody_sewage_bck,ruined_passage_dark_bck,prayer_room_bck,\
            ship_wreck_bck,violet_bck,graveyard_bck,clean_passage_back]

screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN,pygame.RESIZABLE)

pygame.display.set_caption("1")



wraith_r = [pygame.image.load("resources\\characters\\Wraith_01\\PNG Sequences\\Walking\\%s.png"%frame) for frame in range(1,13)]
wraith_l = [pygame.transform.flip(pygame.image.load("resources\\characters\\Wraith_01\\PNG Sequences\\Walking\\%s.png"%frame), True, False) for frame in range(1,13)]
wraith_idle_r = [pygame.image.load("resources\\characters\\Wraith_01\\PNG Sequences\\Idle Blink\\%s.png"%frame) for frame in range(1,13)]
wraith_idle_l = [pygame.transform.flip(pygame.image.load("resources\\characters\\Wraith_01\\PNG Sequences\\Idle Blink\\%s.png"%frame), True, False) for frame in range(1,13)]

i = 0
for picture in wraith_idle_r:
    wraith_idle_r[i] = pygame.transform.scale(picture, (250, 203))
    i += 1

i = 0
for picture in wraith_idle_l:
    wraith_idle_l[i] = pygame.transform.scale(picture, (250, 203))
    i += 1

class Wraith(pygame.sprite.Sprite):
    def __init__(self, leftimgs, rytimgs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources\\characters\\Wraith_01\\PNG Sequences\\Walking\\1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (0,600)
        self.velocity_x = 0
        self.velocity_y = 0
        self.r_imgs = rytimgs
        self.l_imgs = leftimgs
        self.len_r_imgs = len(self.r_imgs)
        self.len_l_imgs = len(self.l_imgs)
        self.jump = False
        self.jump_power = 8
        self.jumpcount = self.jump_power
        self.right = False
        self.left = False
        self.walking = False
        self.walkcount = 0
        self.idlecount = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.right == True and self.walking == True:
            if self.walkcount < self.len_r_imgs - 1:
                self.image = self.r_imgs[int(self.walkcount)]
                self.walkcount+=0.5
            else:
                self.walkcount = 0

        elif self.left == True and self.walking == True:
            if self.walkcount < self.len_l_imgs - 1:
                self.image = self.l_imgs[int(self.walkcount)]
                self.walkcount += 0.5

            else:
                self.walkcount = 0

        elif self.left == True and self.walking == False:
            if self.idlecount < 11:
                self.image = wraith_idle_l[int(self.idlecount)]
                self.idlecount += 0.2

            else:
                self.idlecount = 0

        elif self.right == True and self.walking == False:
            if self.idlecount < 11:
                self.image = wraith_idle_r[int(self.idlecount)]
                self.idlecount += 0.2

            else:
                self.idlecount = 0

        if self.jump == True:
            if self.jumpcount >= -self.jump_power:
                if self.jumpcount < 0:
                    self.velocity_y = self.jumpcount**2
                    
                else:
                    self.velocity_y = -self.jumpcount**2
                self.jumpcount -= 1

            else:
                self.jump = False
                self.jumpcount = self.jump_power

all_sprites = pygame.sprite.Group()

wraith = Wraith(wraith_l, wraith_r)
all_sprites.add(wraith)

bck_index = 0
running = True

#index_update_constant = 0

def game_loop():
    pygame.mixer.music.play(-1)
    intro = False
    #global wraith_r
    #global wraith_l
    global index_update_constant
    global bck_index
    global running
    while running:

        clock.tick(FPS)
        
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            # Keydown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    wraith.velocity_y = -8

                elif event.key == pygame.K_s:
                    wraith.velocity_y = 8

                if event.key == pygame.K_a:
                    #wraith.image = wraith_l[index_update_constant]
                    wraith.walking = True
                    wraith.right = False
                    wraith.left = True                        
                    wraith.velocity_x = -8

                elif event.key == pygame.K_d:
                    #wraith.image = wraith_r[index_update_constant]
                    wraith.walking = True
                    wraith.right = True
                    wraith.left = False
                    wraith.velocity_x = 8

                if event.key == pygame.K_SPACE:
                    if wraith.jump == False:
                        wraith.jump = True

                if event.key == pygame.K_p:
                    resume_sound.play()
                    pause()
                    
            # Keyup
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    wraith.velocity_y = 0

                elif event.key == pygame.K_s:
                    wraith.velocity_y = 0

                if event.key == pygame.K_a:
                    wraith.walking = False
                    wraith.velocity_x = 0

                elif event.key == pygame.K_d:
                    wraith.walking = False
                    wraith.velocity_x = 0

        #screen.fill((BLACK))
        try:
            screen.blit(bck_list[bck_index], (0,0))
        except:
                bck_index = 0

        if wraith.rect.left > WIDTH:
            wraith.rect.right = 0
            bck_index += 1

        elif wraith.rect.right < 0:
            wraith.rect.left = WIDTH
            bck_index -= 1

        #index_update_constant += 1
        # Update
        all_sprites.update()
        # Draw
        all_sprites.draw(screen)
        # display flip
        pygame.display.flip()



game_intro()
game_loop()

