import mover
import game
import pygame
import math

from pygame.locals import *


class Bounce(game.Game):

    """Bouncing Ball game"""

    def __init__(self):
        super(Bounce, self).__init__()

        self.movers = [
            mover.Mover(self.WINDOWWIDTH, self.WINDOWHEIGHT)
            for _ in range(15000)
            ]

        self.movers = [
            m for m in self.movers
            if self.is_in_circle(m)
            ]

        pygame.mouse.set_visible(False)

    def evnt_hndlr(self, event):
        pass

    def update(self, delta):
        for m in self.movers:
            m.update()

    def draw(self, surf):
        for m in self.movers:
            m.display(surf)

    def is_in_circle(self, m):
        inx = (m.location.x - (self.WINDOWWIDTH / 2)) ** 2
        iny = (m.location.y - (self.WINDOWHEIGHT / 2)) ** 2
        distance = math.sqrt(inx + iny)
        return distance < 200

if __name__ == '__main__':
    b = Bounce()
    b.run()
