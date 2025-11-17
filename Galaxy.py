#galaxy color shift 
#galaxy class 
#particle class
#main 

import random 
import pygame 
import math 

#class particle: represents a single star in the galaxy
class Particle(): 
    def __init__(self, size=4, life=3000, palette=None): 
        self.center = center 
        self.size = size
        self.life = life
        self.age = 0 
        self.dead = False
        self.aplha = 255

        # choose random color from palette
        self.color = random.choice(palette)

        #spiral motion set up 
        self.angle = random.uniform(0,360) #starting angle 
        self.radius = random.uniform(0, 300) #distance from center
        self.angular_speed = random.uniform(10, 60) #degrees per second

        #rotation setup 
        self.rotation = 0 
        self.rotation_speed = random.uniform (30, 180)

        #create triangle surface 
        self.surface = self.update_sruface()
        self.pos = self.compute_position() 