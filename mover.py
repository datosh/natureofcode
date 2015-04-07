import random
import pvector
import pygame


class Mover(object):

    """A simple object that can move"""

    def __init__(self, screen_width, screen_height):
        super(Mover, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.location = pvector.PVector(random.randrange(screen_width),
                                        random.randrange(screen_height))
        self.velocity = pvector.PVector(0, 0)
        self.acceleration = pvector.PVector(0, 0)

        self.mass = 10
        self.max_velo = 40

        self.size = 3

    def update(self):
        # Update the vectors
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.max_velo)
        self.location.add(self.velocity)

        # Keep the mover inside the window
        self.check_edges()

        # Reset the acceleration, so the forces can be added up in the
        # next tick once again
        self.acceleration.mult(0)

    def display(self, surface):
        pygame.draw.rect(surface, pygame.Color('blue'),
                         pygame.Rect(self.location.x, self.location.y,
                                     2 * self.mass, 2 * self.mass))

    def applyForce(self, force):
        '''Adds the force supplied to the acceleration. The force is not
        altered in the process'''
        f = force.copy()  # work on a copy so force is not altered
        f.div(self.mass)
        self.acceleration.add(f)

    def check_edges(self):
        if self.location.x > self.screen_width:
            self.location.x = self.screen_width
            self.velocity.x *= -1
        elif self.location.x < 0:
            self.location.x = 0
            self.velocity.x *= -1

        if self.location.y > self.screen_height:
            self.location.y = self.screen_height
            self.velocity.y *= -1
        elif self.location.y < 0:
            self.location.y = 0
            self.velocity.y *= -1
