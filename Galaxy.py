#galaxy color shift 
#galaxy class 
#particle class
#main 

import random 
import pygame 
import math 

#class particle: represents a single star in the galaxy
class Particle(): 
    def __init__(self, center, size=4, life=3000, palette=None, arm_count=4, arm_spread=0.5): 
        self.center = center  
        self.size = size
        self.life = life
        self.age = 0 
        self.dead = False
        self.aplha = 255

        # choose random color from palette
        self.color = random.choice(palette)

        #spiral arm logic 
        arm = random.randint(0, arm_count - 1)
        theta = random.uniform(0, 6 * math.pi)
        offset = random.uniform(-arm_spread, arm_spread)
        self.angle = (2 * math.pi * arm / arm_count) + theta + offset
        self.radious = 20 + 15 * theta 


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
        self.rotation += self.rotation_speed * (dt / 1000)
        self.pos = self.compute_position() 

        #update spiral angle and rotation 
        self.angle += self.angular_speed * (dt / 1000)
        self.rotation += self.rotation_speed * (dt / 1000)
        self.pos = self.compute_position()
    
    def update_surface(self): 
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        points = [
            (self.size //2, 0),
            (self.size, self.size),
            (0, self.size)
        ]
        pygame.draw.polygon(surface, self.color, points)
        return surface 

    def draw(self, surface): 
        # draw particle on screen 
        if self.dead: 
            return 
        self.surface.set_alpha(self.alpha)
        rotated = pygame.transform.rotate(self.surface, self.rotation)
        rect = rotated.get_rect(center=(self.pos[0], self.pos[1])) 
        surface.blit(rotated, rect.topleft) 
#class galaxy: manages multiple particles and color palettes 
class Galaxy(): 
    # set up galaxy properties 
    def __init__(self, center): 
        self.center = center 
        self.particles = [] 
        self.spawn_rate = 5 
        self.size = 4 
        self.palette_index = 0 

    #define multiple color palettes
        self.palettes = [
            [pygame.Color(255, 255, 255), pygame.Color(200,200 ,255),
             pygame.Color(255,200, 255), pygame.Color(255, 255, 150)],
            [pygame.Color(255, 0, 0), pygame.Color(0, 255, 255),
              pygame.Color(255,0, 255), pygame.Color(255, 255, 0)],
            [pygame.Color(0, 255, 0), pygame.Color(255, 255, 0),
              pygame.Color(255, 128, 0), pygame.Color(128, 0, 255)] 
        ]
    def current_palette(self): 
        #return the current color palette
        return self.palettes[self.palette_index] 
    
    def update(self, dt): 
        #update galaxy each frame 
        self._spawn_particles()
        self.particles = [p for p in self.particles if not p.dead]
        for particle in self.particles: 
            particle.update(dt)

    def _spawn_particles(self):
        #spawn new particles using current palette
        for _ in range(self.spawn_rate):
            particle = Particle(self.center, size=self.size, palette=self.current_palette())
            self.particles.append(particle)

    def shift_palette(self): 
        #shift to the next color palette
        self.palette_index = (self.palette_index + 1) % len(self.palettes)

    def draw(self, surface): 
        #draw all particles 
        for p in self.particles: 
            p.draw(surface)  

def main(): 
    # pygame and screen
    pygame.init()
    pygame.display.set_caption("milky way galaxy") 
    resolution = (1920, 1080) 
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN) 
    galaxy = Galaxy(center=(resolution[0]// 2, resolution[1]//2)) 
    clock = pygame.time.Clock()
    running = True 
    
    #game loop 
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    running = False 
                elif event.key == pygame.MOUSEBUTTONDOWN: 
                    galaxy.shift_palette()

        galaxy.update(dt)
        screen.fill((0, 0, 10))
        galaxy.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__": 
    main() 
