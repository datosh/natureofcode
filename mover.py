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

        # The gravitational constant
        self.G = 0.05

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
