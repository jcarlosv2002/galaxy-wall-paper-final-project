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
        self.surface = self.update_surface()
        self.pos = self.compute_position()  
    
    def compute_position(self):
        x = self.center[0] + self.radius * math.cos(math.radians(self.angle))
        y = self.center[1] + self.radius * math.sin(math.radians(self.angle))
        return (x, y)
    
    def update(self, dt): 
        self.age += dt 
        if self.age >= self.life:
            self.dead = True
        self.alpha = 255 * (1 - (self.age / self.life)) #particle fades out over time and update
        
        #update spiral angle and rotation 
        self.angle += self.angular_speed * (dt / 1000)
        self.rotation += self.rotation_speed * (dt / 1000)
        self.pos = self.compute_position()
    
    def update_surface(self): 
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        points = [
            (self.size //2, 0),
            (self.size. self.size),
            (0, self.size)
        ]
        pygame.draw.polygon(surface, self.color, points)
        return surface 

    def draw(self, sruface): 
        # draw particle on screen 
        if self.dead: 
            return 
        self.surface.set_alpha(self.alpha)
        rotated = pygame.transform.rotate(self.surface, self.rotation)
        rect = rotated.get_rect(center=(self.pos[0], self.pos[1])) 
        surface.blit(rotated, rect.topleft) 
