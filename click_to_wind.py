import mover
import game
import pvector

from pygame.locals import *


class WindyBall(game.Game):

    """Windy Ball game"""

    def __init__(self):
        super(WindyBall, self).__init__()

        self.movers = [mover.Mover(self.WINDOWWIDTH, self.WINDOWHEIGHT)
                       for _ in range(1)]

    def evnt_hndlr(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                wind = pvector.PVector(3, 0)
                for m in self.movers:
                    m.applyForce(wind)
            elif event.button == 3:
                wind = pvector.PVector(-3, 0)
                for m in self.movers:
                    m.applyForce(wind)

    def update(self, delta):
        gravity = pvector.PVector(0, .16)
        for m in self.movers:
            m.applyGravity(gravity)

        for m in self.movers:
            m.update()
            # print(m.velocity.angle())

    def draw(self, surf):
        for m in self.movers:
            m.display(surf)

if __name__ == '__main__':
    b = WindyBall()
    b.run()
