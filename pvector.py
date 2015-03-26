class PVector(object):

    """A 2d (or later 3d) vector for easy calculation."""

    def __init__(self, x=0, y=0):
        super(PVector, self).__init__()
        self.x = x
        self.y = y

    def add(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y


