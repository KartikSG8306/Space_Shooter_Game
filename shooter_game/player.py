import math
from math import atan2 , cos , sin
from pygame import *
width , height = 1000,800

black = (10 ,10 ,15)
neon_green = (50 , 255 ,50)
yellow = (255,255,0)
white = (255,255,255)

player_friction = 0.98
recoil_force = 5.0
player_speed_limit = 10.0
enemy_speed = 2
bullet_speed = 15.0

class Player:
    def __init__(self):
        self.pos = math.Vector2(width//2 , height//2)
        self.vel = math.Vector2(0,0)
        self.angle = 0
        self.radius = 15

    def update(self):
        self.pos+=self.vel

        self.vel *= player_friction

        if self.pos.x <0 or self.pos.x > width:
            self.vel.x *=-1
            self.pos.x = max(0 , min(self.pos.x , width) )
        if self.pos.y <0 or self.pos.y > height:
            self.vel.y *= -1
            self.pos.y = max(0 , min(self.pos.y , height))

        if self.vel.length() > player_speed_limit:
            self.vel.scale_to_length(player_speed_limit)

        mouse_x , mouse_y = mouse.get_pos()
        dx = mouse_x - self.pos.x
        dy = mouse_y - self.pos.y
        self.angle = atan2(dy,dx)

    def shoot(self):
        direction = math.Vector2(cos(self.angle),sin(self.angle))

        self.vel -= direction * recoil_force

        bullet_pos = self.pos + direction*25
        return Bullet(bullet_pos.x , bullet_pos.y , direction)
    def draw(self, surface, offset):
        p_pos = (self.pos.x + offset[0], self.pos.y + offset[1])

        # Gun Barrel
        end_x = p_pos[0] + cos(self.angle) * 30
        end_y = p_pos[1] + sin(self.angle) * 30
        draw.line(surface, (150, 150, 150), p_pos, (end_x, end_y), 8)

        # Body
        draw.circle(surface, neon_green, (int(p_pos[0]), int(p_pos[1])), self.radius)
        draw.circle(surface, black, (int(p_pos[0]), int(p_pos[1])), 5)

class Bullet:
    def __init__(self,x,y,direction):
        self.pos = math.Vector2(x,y)
        self.vel = direction*bullet_speed
        self.radius = 4
    def update(self):
        self.pos+=self.vel
    def draw(self, surface, offset):
        draw.circle(surface, yellow, (int(self.pos.x + offset[0]), int(self.pos.y + offset[1])), self.radius)







