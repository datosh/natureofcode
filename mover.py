import math
import pvector
import pygame


class Mover(object):

    """A simple object that can move"""

    def __init__(self, x, y):
        super(Mover, self).__init__()

        self.location = pvector.PVector(x, y)
        self.velocity = pvector.PVector(0, 0)
        self.acceleration = pvector.PVector(0, 0)

        self.mass = 1
        self.max_velo = 40
        self.do_limit = False

        # The gravitational constant for attraction
        self.G = 0.05

    def update(self):
        # Update the vectors
        self.velocity.add(self.acceleration)
        if self.do_limit:
            self.velocity.limit(self.max_velo)
        self.location.add(self.velocity)

        # Reset the acceleration, so the forces can be added up in the
        # next tick once again
        self.acceleration.mult(0)

    def display(self, surface):
        '''Is used to display a dummy, the display function should be
        overwritten when extending this class. Here we just show a rectangle
        that grows, the more mass the mover object has'''

        width = 1 * self.mass
        height = 1 * self.mass

        # get the angle and convert to degrees
        angle = self.velocity.angle()
        angle = math.degrees(angle)

        # Draw rect on a new surface
        rect_image = pygame.Surface((width, height))
        rect_image.set_colorkey(pygame.Color('black'))
        pygame.draw.rect(rect_image, pygame.Color('blue'),
                         [0, 0, width, height])
        pygame.draw.rect(rect_image, pygame.Color('red'),
                         [0, height - 5, width, 5])

        # rotate the image
        rect_image = pygame.transform.rotate(rect_image, angle)

        surface.blit(rect_image, (self.location.x, self.location.y))

        # pygame.draw.rect(surface, pygame.Color('blue'),
        #                  pygame.Rect(self.location.x, self.location.y,
        #                              2.3 * self.mass, 1.1 * self.mass))

    def applyForce(self, force):
        ''' force = PVector

        Adds the force supplied to the acceleration. The force is not
        altered in the process'''

        f = force.copy()  # work on a copy so force is not altered
        f.div(self.mass)
        self.acceleration.add(f)

    def applyFriction(self, c):
        ''' c = Integer

        c is the friction coefficient. it determines how strong of friction
        is going to be applied to the movement of the character.'''

        # Calculate the strength of the friction
        normal = 1  # TODO: calculate the normal correctly to the formula
        mag = c * normal

        # Calculate the direction of the friction
        friction = self.velocity.copy()
        friction.mult(-1)
        friction.normalize()

        # Combine magnitude and direction
        friction.mult(mag)

        self.applyForce(friction)

    def applyGravity(self, gravity):
        ''' gravity = PVector

        This method is used to apply a mass independant force, i.e.,
        gravity, to the mover object. The gravity vector is not altered
        in the process'''

        g = gravity.copy()
        g.mult(self.mass)
        self.applyForce(g)

    def attract(self, otherMover):
        '''Uses the gravitational constant of this object to compute and apply
        the gravitational force between this object and the supplied otherMover
        object.'''
        MAX_DISTANCE = 25
        MIN_DISTANCE = 1

        force1 = pvector.PVector.s_sub(otherMover.location, self.location)

        distance = force1.mag()

        # Disable gravitational force for distant objects, since it is almost
        # not noticable
        if distance > MAX_DISTANCE:
            return
        # For really small distances the gravitational force gets really
        # huge so we contrain it to a minimal value.
        if distance < MIN_DISTANCE:
            distance = MIN_DISTANCE

        # Calculate the strength of the force
        mag = (self.G * self.mass * otherMover.mass) / (distance * distance)

        force1.normalize()
        force2 = force1.copy()

        force1.mult(mag)
        force2.mult(-mag)

        self.applyForce(force1)
        otherMover.applyForce(force2)
