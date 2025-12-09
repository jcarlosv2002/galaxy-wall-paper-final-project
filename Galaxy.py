#galaxy color shift 
#galaxy class 
#particle class
#main 

import random
import pygame
import math

def lerp_color(c1, c2, t):
    r = int(c1.r + (c2.r - c1.r) * t)
    g = int(c1.g + (c2.g - c1.g) * t)
    b = int(c1.b + (c2.b - c1.b) * t)
    return pygame.Color(r, g, b)

class Particle():
    def __init__(self, center, size=4, palette=None, arm_count=5, arm_spread=0.2, i=None, arm=None):
        self.center = center
        self.depth = random.uniform(0.5, 1.5)
        self.size = int(size * self.depth)
        self.color = random.choice(palette)
        self.alpha = int(180 * self.depth)
        self.i = i
        self.arm = arm
        self.arm_count = arm_count

        if i is not None and arm is not None:
            theta = i * 0.25
            base_angle = (2 * math.pi * arm) / arm_count
            radial_noise = math.sin(theta * 0.25 + arm) * 8 * random.uniform(0.5, 1.0)
            self.radius = 20 + 4 * theta + radial_noise + random.uniform(-10, 10)
            angular_noise = math.cos(theta * 0.15) * 0.2
            self.angle = base_angle + theta + angular_noise + random.uniform(-arm_spread, arm_spread)

            if i < 100:
                self.radius = random.uniform(0, 30)
                self.angle = random.uniform(0, 2 * math.pi)
        else:
            self.angle = random.uniform(0, 2 * math.pi)
            self.radius = random.uniform(0, 40)

        self.rotation = 0
        self.rotation_speed = random.uniform(30, 180)
        self.surface = self.update_surface()
        self.pos = self.compute_position()

    def compute_position(self):
        x = self.center[0] + self.radius * math.cos(self.angle)
        y = self.center[1] + self.radius * math.sin(self.angle)
        return (x, y)

    def update(self, dt, global_rotation_speed=0):
        self.angle += global_rotation_speed * (dt / 1000)
        self.rotation += self.rotation_speed * (dt / 1000)
        self.pos = self.compute_position()

    def update_surface(self):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surface

    def draw(self, surface):
        self.surface.set_alpha(self.alpha)
        rotated = pygame.transform.rotate(self.surface, self.rotation)
        rotated.set_alpha(self.alpha)
        rect = rotated.get_rect(center=(self.pos[0], self.pos[1]))
        surface.blit(rotated, rect.topleft)

class Galaxy():
    def __init__(self, center):
        self.center = center
        self.particles = []
        self.spawn_rate = 60
        self.size = 4
        self.palette_index = 0
        self.arm_count = 5
        self.arm_spread = 0.2
        self.global_index = 0
        self.global_rotation_speed = 0.15
        self.max_particles = 4000

        self.palettes = [
            [pygame.Color(255, 255, 255), pygame.Color(200, 200, 255),
             pygame.Color(255, 200, 255), pygame.Color(255, 255, 150)],
            [pygame.Color(255, 0, 0), pygame.Color(0, 255, 255),
             pygame.Color(255, 0, 255), pygame.Color(255, 255, 0)],
            [pygame.Color(0, 255, 0), pygame.Color(255, 255, 0),
             pygame.Color(255, 128, 0), pygame.Color(128, 0, 255)]
        ]

        self.transitioning = False
        self.transition_time = 2000
        self.transition_elapsed = 0
        self.old_palette = None
        self.new_palette = None

    def current_palette(self):
        return self.palettes[self.palette_index]

    def shift_palette(self):
        self.old_palette = self.current_palette()
        self.palette_index = (self.palette_index + 1) % len(self.palettes)
        self.new_palette = self.current_palette()
        self.transitioning = True
        self.transition_elapsed = 0

    def update(self, dt):
        if len(self.particles) < self.max_particles:
            self._spawn_particles()

        if self.transitioning:
            self.transition_elapsed += dt
            t = min(1.0, self.transition_elapsed / self.transition_time)
            for p in self.particles:
                target = random.choice(self.new_palette)
                p.color = lerp_color(p.color, target, t)
                p.surface = p.update_surface()
            if t >= 1.0:
                self.transitioning = False

        for particle in self.particles:
            particle.update(dt, self.global_rotation_speed)

    def _spawn_particles(self):
        for arm in range(self.arm_count):
            for _ in range(self.spawn_rate):
                i = self.global_index
                particle = Particle(
                    center=self.center,
                    size=self.size,
                    palette=self.current_palette(),
                    arm_count=self.arm_count,
                    arm_spread=self.arm_spread,
                    i=i,
                    arm=arm
                )
                self.particles.append(particle)
                self.global_index += 1

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Milky Way Galaxy")
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    galaxy = Galaxy(center=(resolution[0] // 2, resolution[1] // 2))
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    galaxy.shift_palette()
                elif event.key == pygame.K_UP:
                    galaxy.arm_spread += 0.05
                elif event.key == pygame.K_DOWN:
                    galaxy.arm_spread = max(0.05, galaxy.arm_spread - 0.05)
                elif event.key == pygame.K_RIGHT:
                    galaxy.global_rotation_speed += 0.05
                elif event.key == pygame.K_LEFT:
                    galaxy.global_rotation_speed = max(0.0, galaxy.global_rotation_speed - 0.05)
                elif event.key == pygame.K_s:
                    galaxy.spawn_rate += 10
                elif event.key == pygame.K_a:
                    galaxy.spawn_rate = max(10, galaxy.spawn_rate - 10)

        galaxy.update(dt)
        screen.fill((0, 0, 10))
        galaxy.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main() 