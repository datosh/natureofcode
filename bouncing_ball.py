import game
import pygame


class Ball(object):

    """A simple ball"""

    def __init__(self, x, y, xspeed, yspeed):
        super(Ball, self).__init__()

        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed


class Bounce(game.Game):

    """Bouncing Ball game"""

    def __init__(self):
        super(Bounce, self).__init__()

        self.ball = Ball(100, 100, 5, 5)

    def evnt_hndlr(self, event):
        pass

    def update(self, delta):
        ball = self.ball

        ball.x += ball.xspeed
        ball.y += ball.yspeed

        if ball.x > self.WINDOWWIDTH or ball.x < 0:
            ball.xspeed *= -1
        if ball.y > self.WINDOWHEIGHT or ball.y < 0:
            ball.yspeed *= -1

    def draw(self, surf):
        ball = self.ball
        pygame.draw.rect(
            surf,
            pygame.Color('blue'),
            pygame.Rect(ball.x, ball.y, 5, 5))

if __name__ == '__main__':
    b = Bounce()
    b.run()
