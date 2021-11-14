#!/usr/bin/env python

import pygame
import sys
import time
import random

from pygame.locals import *

FPS = 10
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface1 = pygame.Surface(screen.get_size())
surface1 = surface1.convert()
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE=10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)

#INSIDE OF THE GAME LOOP
screen.blit(surface, (0,0))

def draw_cloud(surf, color, pos):
    cloudImg = pygame.image.load("cloud.png")
    cloudImg = pygame.transform.scale(cloudImg, (50, 50))
    surf.blit(cloudImg, (pos[0],pos[1]))


def draw_rain(surf, color, pos):
     rainImg = pygame.image.load("rains.png")
     rainImg = pygame.transform.scale(rainImg, (60, 60))
     surf.blit(rainImg, (pos[0],pos[1]))

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.font.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text, text_rgb, bg_rgb)
    return surface.convert_alpha()

class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text,  pos, font, bg="black"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont(None, font)
        self.set_text(text)

    def show(self):
        screen.blit(button1.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
    def set_text(self, text, bg=(65,105,225)):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("Pink"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


class Clouds(object):
    def __init__(self):
        self.lose()
        self.color = (0,0,0)
        self.gameOver = False

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surf):
        for p in self.positions:
            draw_cloud(surf, self.color, p)



class Cloud(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-15) * GRIDSIZE, random.randint(0, GRID_HEIGHT-15) * GRIDSIZE)

    def draw(self, surf):
        draw_cloud(surf, self.color, self.position)

class Rain(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(5, GRID_WIDTH-5) * GRIDSIZE-5, random.randint(5, GRID_HEIGHT-5) * GRIDSIZE-5)

    def draw(self, surf):
        draw_rain(surf, self.color, self.position)

def check_eat(clouds, cloud):
    if clouds.get_head_position()[0] < cloud.position[0] + 20 and clouds.get_head_position()[0] > cloud.position[0] - 20 and clouds.get_head_position()[1] < cloud.position[1] + 20 and clouds.get_head_position()[1] > cloud.position[1] - 20 :
            clouds.length += 1
            cloud.randomize()

def check_rain(clouds, cloud):
    if clouds.get_head_position()[0] < rain.position[0] + 20 and clouds.get_head_position()[0] > rain.position[0] - 20 and clouds.get_head_position()[1] < rain.position[1] + 50 and clouds.get_head_position()[1] > rain.position[1] - 20 :
            clouds.length -= 1
            clouds.positions.pop()
            rain.randomize()
    if(len(clouds.positions) == 0):
        clouds.gameOver = True

if __name__ == '__main__':

    button1 = Button(
        "Begin",
        (75, 250),
        font=50,
        bg="navy",)
    clicked = False
    while not clicked:
        surface.fill((255,255,255))
        surface = pygame.image.load("colors.jpeg")
        surface = pygame.transform.scale(surface, (700, 700))
        font = pygame.font.Font(None, 70)
        text = font.render("Cloud Collector", 1, (65,105,225))
        textpos = text.get_rect()
        textpos.centerx = 300
        textpos.centery = 50

        font1 = pygame.font.Font(None, 25)
        text1 = font1.render("Use your arrow keys to collect clouds and avoid the rain ", 1, (65,105,225))
        # textpos1 = text.get_rect()
        # textpos1.centerx = 300
        # textpos1.centery = 200


        font2 = pygame.font.Font(None, 25)
        text2 = font2.render("If you run into yourself, you'll lose all the clouds you've collected", 1, (65, 105, 225))
        # textpos2 = text.get_rect()
        # textpos2.centerx = 300
        # textpos2.centery = 250

        font3 = pygame.font.Font(None, 25)
        text3 = font3.render("Rain takes away one of your clouds! Don't let your cloud count reach zero!", 1, (65, 105, 225))
        # textpos3 = text.get_rect()
        # textpos3.centerx = 300
        # textpos3.centery = 300

        surface.blit(text, textpos)
        surface.blit(text1, (10, 100))
        surface.blit(text2, (10, 150))
        surface.blit(text3, (10, 200))
        screen.blit(surface, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            clicked = button1.click(event)
        button1.show()
        clock.tick(30)
        pygame.display.update()

    clouds = Clouds()
    cloud = Cloud()

    rain = Rain()
    rains = []
    rains.append(rain)

    passedTime = 0;
    incrementsOfTen = 0;


    while not clouds.gameOver:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    clouds.point(UP)
                elif event.key == K_DOWN:
                    clouds.point(DOWN)
                elif event.key == K_LEFT:
                    clouds.point(LEFT)
                elif event.key == K_RIGHT:
                    clouds.point(RIGHT)


        surface.fill((255,255,255))
        surface = pygame.image.load("colors.jpeg")
        surface = pygame.transform.scale(surface, (700, 700))
        clouds.move()
        check_eat(clouds, cloud)
        for rain in rains:
            check_rain(clouds, rain)
            if(clouds.gameOver == True):
                continue
        clouds.draw(surface)
        for rain in rains:
            rain.draw(surface)
        cloud.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(clouds.length), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + clouds.length/3)


        if ((pygame.time.get_ticks() / 1000) % 7 < .09):
            for rain in rains:
                rain.randomize()
            cloud.randomize()
        if(clouds.length == 1):
            incrementsOfTen = 0
        if (clouds.length - (incrementsOfTen*10) == 10):
            rain2 = Rain()
            rains.append(rain2)
            incrementsOfTen += 1

    count = 0
    while count < 25:
        surface1.fill((255,255,255))
        surface1 = pygame.image.load("colors.jpeg")
        surface1 = pygame.transform.scale(surface1, (700, 700))
        font = pygame.font.Font(None, 70)
        text = font.render("Game Over!", 1, (65,105,225))
        textpos = text.get_rect()
        textpos.centerx = 300
        textpos.centery = 50
        surface1.blit(text, textpos)
        screen.blit(surface1, (0,0))
        pygame.display.update()
        count += 1

    pygame.display.quit()
    pygame.quit()
