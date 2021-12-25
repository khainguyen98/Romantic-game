import pygame
import random
import math
from pygame import mixer

pygame.init()

FPS = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.png')

# you
khaiImg = []
khaiX = []
khaiY = []
khaiX_change = []
khaiY_change = []
num_of_khai = 5

for i in range(num_of_khai):
    khaiImg.append(pygame.image.load('khai.png'))
    khaiX.append(random.randint(0,735))
    khaiY.append(random.randint(20,150))
    khaiX_change.append(0.2)
    khaiY_change.append(20)

    def khai(x,y,i):
        screen.blit(khaiImg[i],(x,y))

# your girl friend
haImg = pygame.image.load('ngan.png')
haX = 380
haY = 500
haX_change = 0
Y_change = 0

def ha(x,y):
    screen.blit(haImg,(x,y))

# heart
heartImg = pygame.image.load('heart.png')
heartX = 0
heartY = haY
heartX_change = 0
heartY_change = 0.4

heart_state = "ready"

def heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heartImg,(x+16,y+10))

# icon and title
title = pygame.display.set_caption("AnhYêuEm")
icon = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

# check colision
def iscollision(haiX,haiY,heartX,heartY):
    distance = math.sqrt(math.pow(haiX - heartX,2)+math.pow(haiY - heartY,2))

    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Yêu Anh x " + str(score_value),True, (150,150,255))
    screen.blit(score,(x,y))

# Game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("You lost but I still love u" ,True, (150,150,255))
    screen.blit(over_text,(30,250))

# sound and music
mixer.music.load("cauhon.wav")
mixer.music.play(-1)

running = True
while running:

    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                haX_change = 1
            if event.key == pygame.K_LEFT:
                haX_change = -1
            if event.key == pygame.K_UP:
                haY_change = -1
            if event.key == pygame.K_DOWN:
              change = 1
            if event.key == pygame.K_SPACE:
                if heart_state == "ready":
                    heartX = haX
                    heartY = Y
                    heart(heartX,heartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                haX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                haY_change = 0

    ha(haX,haY)
    haX += haX_change
    Y += haY_change

    if haX <=0:
        haX = 0 
    elif haX >=736:
        haX = 736

    if haY <= 400: 
        haY = 400
    elif haY >=530:
        haY = 529

    for i in range(num_of_khai):
        # game over
        if khaiY[i] > 200:
            for j in range(num_of_khai):
                khaiY[j] =2000
            game_over_text()
            break

        khai(khaiX[i],khaiY[i],i)

        if khaiX[i] <= 0:
            khaiX_change[i] = 0.2
            khaiY[i] += khaiY_change[i]
        if khaiX[i] >= 736:
            khaiX_change[i] = -0.2
            khaiY[i] += khaiY_change[i]

        khaiX[i] += khaiX_change[i]
           
        collision = iscollision(khaiX[i],khaiY[i],heartX,heartY)
        if collision:
            heart_state = "ready"
            khaiY[i] = random.randint(50,150)
            khaiX[i] = random.randint(0,735)
            score_value += 1
            explosion_sound = mixer.Sound('tick.wav')
            explosion_sound.play()

    if heartY <= 0:
        heartY = Y
        heart_state ="ready" 
    if heart_state == "fire":
        heartY -= heartY_change
        heart(heartX,heartY)

    show_score(textX,textY)
    fpsclock.tick()
    pygame.display.flip()
