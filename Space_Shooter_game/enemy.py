import math
from pygame import *
import random
width , height = 1000,800

black = (10 ,10 ,15)
neon_green = (50 , 255 ,50)
yellow = (255,255,0)
white = (255,255,255)
neon_red = (255 ,50 ,50)

player_friction = 0.98
recoil_force = 5.0
player_speed_limit = 10.0
enemy_speed = 2
bullet_speed = 15.0

class Enemy:
    def __init__(self):
        side = random.choice(['top','bottom','left','right'])
        if side == 'top':
            x , y =random.randint(0 ,width), -50
        elif side == 'bottom':
            x , y = random.randint(0 ,width), height + 50
        elif side == 'left':
            x,y = -50 ,random.randint(0 ,height)
        else :
            x,y=width +50 , random.randint(0,height)

        self.pos = math.Vector2(x,y)
        self.radius = 15
    def update(self,player_pos):
        direction = (player_pos-self.pos)
        if direction.length() > 0:
            direction =direction.normalize()
        self.pos+=direction*enemy_speed

    def draw(self,screen,offset):
        rect = Rect(self.pos.x -10 + offset[0] , self.pos.y -10 + offset[1] , 20,20)
        draw.rect(screen ,neon_red , rect)

class Particle:
    def __init__(self,x,y,color):
        self.pos = [x , y]
        self.vel = [random.uniform(-3 ,3),random.uniform(-3 , 3)]
        self.timer = random.randint(20 , 40)
        self.color = color
        self.size = random.randint(3 , 6)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.timer -=1
        self.size -= 0.1
    def draw(self,screen , offset):
        if self.timer>0:
            rect = (int(self.pos[0] + offset[0]), int(self.pos[1] + offset[1]) , int(self.size), int(self.size))
            draw.rect(screen , self.color ,rect)








