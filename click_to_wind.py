import mover
import game
import pvector

from pygame.locals import *


class WindyBall(game.Game):

    """Windy Ball game"""

    def __init__(self):
        super(WindyBall, self).__init__()

        self.mover = mover.Mover(self.WINDOWWIDTH, self.WINDOWHEIGHT)

    def evnt_hndlr(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                wind = pvector.PVector(3, 0)
                self.mover.applyForce(wind)
            elif event.button == 3:
                wind = pvector.PVector(-3, 0)
                self.mover.applyForce(wind)

    def update(self, delta):
        gravity = pvector.PVector(0, .86)
        self.mover.applyForce(gravity)

        self.mover.update()

    def draw(self, surf):
        self.mover.display(surf)

if __name__ == '__main__':
    b = WindyBall()
    b.run()
