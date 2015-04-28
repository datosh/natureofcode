import math


class PVector(object):

    """A 2d (or later 3d) vector for easy calculation."""

    def __init__(self, x=0, y=0, isCartesian=True):
        super(PVector, self).__init__()
        if isCartesian:
            self.x = x
            self.y = y
        else:
            r = x
            theta = y
            self.x = r * math.sin(theta)
            self.y = r * math.cos(theta)

    def __str__(self):
        return 'x: {0:2f}, y: {1:2f}'.format(self.x, self.y)

    def set(self, x, y):
        '''Sets the values of x and y accordingly'''
        self.x = x
        self.y = y

    def add(self, v):
        '''Add another vector v to this vector'''
        self.x = self.x + v.x
        self.y = self.y + v.y

    @staticmethod
    def s_add(a, b):
        '''Adds the supplied vectors and returns a new vector object'''
        return PVector(a.x + b.x, a.y + b.y)

    def sub(self, v):
        '''Substract another vector v from this vector'''
        self.x = self.x - v.x
        self.y = self.y - v.y

    @staticmethod
    def s_sub(a, b):
        '''Subtracts b from a (a-b) and returns a new vector object'''
        return PVector(a.x - b.x, a.y - b.y)

    def mult(self, n):
        '''Multiply the vector with the scalar n'''
        self.x = self.x * n
        self.y = self.y * n

    @staticmethod
    def s_mult(a, n):
        '''Multiplies both parts of the vector with n, and returns a new vector
        object'''
        return PVector(a.x * n, a.y * n)

    def div(self, n):
        '''Divide the vector by the scalar n'''
        self.x = self.x / n
        self.y = self.y / n

    def mag(self):
        '''Returns the magnitude of the vector'''
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        '''Normalizes this vector.'''
        m = self.mag()
        if m:
            self.div(m)

    def limit(self, max):
        '''Limits the vector to the supplied max value'''
        if self.mag() > max:
            self.normalize()
            self.mult(max)

    def copy(self):
        '''Returns a deep copy of the PVector object'''
        return PVector(self.x, self.y)

    def angle(self):
        '''Returns the angle of the vector in radians.'''
        return math.atan2(self.x, self.y)
