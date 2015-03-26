import game
import noise
import random
import pygame

from pygame.locals import *


class NoiseCreator(object):

    """???"""

    def __init__(self, screen_width, screen_height):
        super(NoiseCreator, self).__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.Surface([640, 480])

    def display(self, surface):
        surface.blit(self.image, (0, 0))

    def generate(self, octaves, persistance, lacunarity):
        base_x = random.randint(0, 100)
        base_y = random.randint(0, 100)

        for x in range(self.screen_width):
            for y in range(self.screen_height):
                xoff = (x / self.screen_width * 7) + base_x
                yoff = (y / self.screen_height * 7) + base_y
                color = int(abs(noise.pnoise2(
                    xoff, yoff,
                    octaves,
                    persistance,
                    lacunarity) * 3333))
                self.image.set_at(
                    (x, y),
                    (color % 255, color % 255, color % 255))


class SimpleWindow(game.Game):

    """Simple Window to display stuff"""

    def __init__(self):
        super(SimpleWindow, self).__init__()
        self.overwrite = True
        self.FPS = 1

        self.nc = NoiseCreator(self.WINDOWWIDTH, self.WINDOWHEIGHT)
        self.nc.generate(1, 0.5, 2)

    def update(self, delta):
        octaves = 2
        persistance = .4
        lacunarity = 3
        print(octaves, persistance, lacunarity)
        self.nc.generate(octaves, persistance, lacunarity)

    def evnt_hndlr(self, event):
        pass

    def draw(self, surf):
        self.nc.display(surf)

if __name__ == '__main__':
    simpleWindow = SimpleWindow()
    simpleWindow.run()
