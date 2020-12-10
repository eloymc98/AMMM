"""
AMMM Project
Location class.
Eloy Marín, Pablo Pazos
"""

class Location(object):
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getId(self):
        return self.id

    def __str__(self):
        return "Location: (%d, %d)" % (self.x, self.y)
