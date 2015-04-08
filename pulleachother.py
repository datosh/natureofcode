import mover
import game

from pygame.locals import *


class PullEachOther(game.Game):

    """Windy Ball game"""

    def __init__(self):
        super(PullEachOther, self).__init__()

        self.movers = [mover.Mover(self.WINDOWWIDTH, self.WINDOWHEIGHT)
                       for _ in range(2)]

    def evnt_hndlr(self, event):
        pass

    def update(self, delta):
        self.movers[0].attract(self.movers[1])

        for m in self.movers:
            m.update()

    def draw(self, surf):
        for m in self.movers:
            m.display(surf)

if __name__ == '__main__':
    b = PullEachOther()
    b.run()
