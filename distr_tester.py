import game
import random
import pygame

from pygame.locals import *


class DistributionTester(object):

    """Shows the random distribution of random"""

    def __init__(self, screen_width):
        super(DistributionTester, self).__init__()

        self.max_number = 48

        self.randomnumbers = [
            pygame.Rect(
                x * screen_width / self.max_number,
                0,
                screen_width / self.max_number,
                1)
            for x in range(self.max_number)
            ]

    def random_tick(self):
        self.randomnumbers[random.randint(0, self.max_number - 1)].height += 1

    def bell_tick(self):
        choice = int(random.gauss(self.max_number / 2, self.max_number / 4))
        if choice >= self.max_number or choice < 0:
            return
        else:
            self.randomnumbers[choice].height += 1

    def monte_carlo_tick(self):
        choice = 0
        while True:
            r1 = random.uniform(0, 1)
            prob = r1
            r2 = random.uniform(0, 1)

            if r2 < prob:
                choice = r1
                choice = int(choice * self.max_number)
                break
        if choice >= self.max_number or choice < 0:
            return
        else:
            self.randomnumbers[choice].height += 1

    def tick(self):
        self.monte_carlo_tick()

    def draw(self, surf):
        for r in self.randomnumbers:
            pygame.draw.rect(surf, pygame.Color('blue'), r)


class SimpleWindow(game.Game):

    """Simple Window to display stuff"""

    def __init__(self):
        super(SimpleWindow, self).__init__()
        self.overwrite = False
        self.FPS = 1200

        self.tester = DistributionTester(self.WINDOWWIDTH)

    def update(self, delta):
        self.tester.tick()

    def evnt_hndlr(self, event):
        pass

    def draw(self, surf):
        self.tester.draw(surf)

if __name__ == '__main__':
    simpleWindow = SimpleWindow()
    simpleWindow.run()
