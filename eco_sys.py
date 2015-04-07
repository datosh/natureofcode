import math
import game
import pygame
import pvector
import random

from pygame.locals import *


class Ecosys(game.Game):

    """The eco system"""

    def __init__(self):
        super(Ecosys, self).__init__()

        self.snake = Snake(self.WINDOWWIDTH, self.WINDOWHEIGHT)

    def evnt_hndlr(self, event):
        pass

    def update(self, delta):
        self.snake.update()

    def draw(self, surf):
        self.snake.draw(surf)


class Snake(object):

    """Implements the movement pattern of a snake"""

    def __init__(self, screen_width, screen_height):
        super(Snake, self).__init__()

        self.base_acc = 0.3
        self.max_velocity = 2

        self.v_location = pvector.PVector(30, 200)
        self.v_velocity = pvector.PVector(0, 0)
        self.v_acceleration = pvector.PVector(self.base_acc, self.base_acc)

        self.size = 3

        self.time = math.pi

    def evnt_hndlr(self, event):
        pass

    def update(self):
        self.time += math.pi / 20
        sine = math.sin(self.time) / 2
        v_sine = pvector.PVector(0, sine)
        self.v_acceleration.set(self.base_acc, self.base_acc)
        self.v_acceleration.add(v_sine)

        print(self.v_acceleration)

        # Apply acceleration to velocity and location. Also limit speed
        self.v_velocity.add(self.v_acceleration)
        self.v_velocity.limit(self.max_velocity)
        self.v_location.add(self.v_velocity)

    def draw(self, surf):
        pos = (int(self.v_location.x), int(self.v_location.y))
        pygame.draw.circle(surf, pygame.Color('green'), pos, self.size)

if __name__ == '__main__':
    e = Ecosys()
    e.run()
