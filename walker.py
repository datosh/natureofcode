import game
import noise
import random
import pygame

from pygame.locals import *


class Walker(object):

    """???"""

    def __init__(self, screen_width, screen_height):
        super(Walker, self).__init__()

        self.x = screen_width / 2
        self.y = screen_height / 2

        self.rect = pygame.Rect(0, 0, 12, 12)
        self.rect.center = (self.x, self.y)

        self.t_x = 0
        self.t_y = 2

    def display(self, surface):
        pygame.draw.rect(surface, pygame.Color('blue'), self.rect)

    def random_step(self):
        step_size = 1

        choice = random.randint(0, 4)
        if choice == 0:
            self.rect.x += step_size
        elif choice == 1:
            self.rect.x -= step_size
        elif choice == 2:
            self.rect.y += step_size
        else:
            self.rect.y -= step_size

    def to_mouse_step(self):
        (x, y) = pygame.mouse.get_pos()
        if x > self.rect.x:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        if y > self.rect.y:
            self.rect.y += 1
        else:
            self.rect.y -= 1

    def perlin_step(self):
        self.rect.x = noise.pnoise1(self.t_x, 2, 1.3) * 300 + 300
        self.rect.y = noise.pnoise1(self.t_y, 2, 1.3) * 240 + 240
        self.t_x += .01
        self.t_y += .01

    def step(self):
        self.perlin_step()


class SimpleWindow(game.Game):

    """Simple Window to display stuff"""

    def __init__(self):
        super(SimpleWindow, self).__init__()
        self.overwrite = True
        self.FPS = 60

        self.walker = Walker(self.WINDOWWIDTH, self.WINDOWHEIGHT)

    def update(self, delta):
        self.walker.step()

    def evnt_hndlr(self, event):
        pass

    def draw(self, surf):
        self.walker.display(surf)

if __name__ == '__main__':
    simpleWindow = SimpleWindow()
    simpleWindow.run()
