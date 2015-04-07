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

        self.max_velo = 4

        self.size = 3

    def update(self):
        # Reenable this line to get the rects follow the mouse
        # mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (self.screen_width / 2 + 0.05,
                     self.screen_height / 2 + 0.05)
        v_mouse = pvector.PVector(mouse_pos[0], mouse_pos[1])

        self.acceleration = pvector.PVector.s_sub(v_mouse, self.location)
        self.max_velo = (1 / (self.acceleration.mag() ** 2)) * 150000
        self.acceleration.normalize()
        self.acceleration.mult(0.25)

        self.velocity.add(self.acceleration)
        self.velocity.limit(self.max_velo)
        self.location.add(self.velocity)

        self.check_edges()

    def display(self, surface):
        pygame.draw.rect(surface, pygame.Color('blue'),
                         pygame.Rect(self.location.x, self.location.y, 2, 2))

    def check_edges(self):
        if self.location.x > self.screen_width:
            self.location.x = 0
        elif self.location.x < 0:
            self.location.x = self.screen_width

        if self.location.y > self.screen_height:
            self.location.y = 0
        elif self.location.y < 0:
            self.location.y = self.screen_height
