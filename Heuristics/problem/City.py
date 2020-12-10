"""
AMMM Project
City class.
Eloy Marín, Pablo Pazos
"""


class City(object):
    def __init__(self, location, population):
        self.location = location
        self.population = population

    def getLocation(self):
        return self.location

    def getPopulation(self):
        return self.population

    def getId(self):
        return self.location.getId()

    def __str__(self):
        return "Location: (%d, %d)" % (self.x, self.y)