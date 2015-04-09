import mover
import game
import pygame
import pvector
import math

from pygame.locals import *


class Canon(object):

    """The canon... duh"""

    def __init__(self, bottomleft):
        super(Canon, self).__init__()
        self.bottomleft = bottomleft

        # Fixed size of the canon
        self.width = 75
        self.height = 25

        # Angle of the canon
        self.angle = 45
        self.max_angle = 80
        self.min_angle = 10

        self.change_angle = 0

        # Initialize the image of the canon
        self.image = pygame.Surface((self.width, self.height))

        # Calculate the spawn position of the next mover
        self.spawnpos = pvector.PVector(0, 0)

    def update(self):
        self.angle += self.change_angle
        if self.angle > self.max_angle:
            self.angle = self.max_angle
        elif self.angle < self.min_angle:
            self.angle = self.min_angle

        # Calculate the spawn position of the next mover
        spawn_x = self.width * math.cos(math.radians(-self.angle))
        spawn_x += self.bottomleft[0]
        spawn_y = self.width * math.sin(math.radians(-self.angle))
        spawn_y += self.bottomleft[1]
        self.spawnpos = pvector.PVector(spawn_x, spawn_y)

    def draw(self, surf):
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey(pygame.Color('black'))
        pygame.draw.rect(self.image, pygame.Color('green'),
                         [0, 0, self.width, self.height])
        self.image = pygame.transform.rotate(self.image, self.angle)

        rect = self.image.get_rect()
        rect.bottomleft = self.bottomleft
        surf.blit(self.image, rect)

        pygame.draw.rect(surf, pygame.Color('red'),
                         [self.spawnpos.x, self.spawnpos.y, 5, 5])

    def shoot(self):
        m = mover.Mover(self.spawnpos.x, self.spawnpos.y)
        init_velocity_mag = 20
        init_velocity = pvector.PVector(init_velocity_mag,
                                        math.radians(self.angle+90),
                                        False)
        m.velocity.add(init_velocity)
        return m


class AimAndShoot(game.Game):

    """Bouncing Ball game"""

    def __init__(self):
        super(AimAndShoot, self).__init__()

        self.c = Canon((10, self.WINDOWHEIGHT - 10))

        self.movers = []

    def evnt_hndlr(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.c.change_angle = 1
            if event.key == K_s:
                self.c.change_angle = -1
            if event.key == K_SPACE:
                self.movers.append(self.c.shoot())
        if event.type == KEYUP:
            if event.key == K_w:
                self.c.change_angle = 0
            if event.key == K_s:
                self.c.change_angle = 0

    def update(self, delta):
        self.c.update()

        gravity = pvector.PVector(0, .51)
        for m in self.movers:
            m.applyGravity(gravity)
            m.applyFriction(1)
            m.update()

    def draw(self, surf):
        self.c.draw(surf)

        for m in self.movers:
            m.display(surf)


if __name__ == '__main__':
    aas = AimAndShoot()
    aas.run()
