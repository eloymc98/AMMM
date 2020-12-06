class City(object):
    def __init__(self, id, location, population):
        self.id = id
        self.location = location
        self.population = population

    def getId(self):
        return self.id

    def getLocation(self):
        return self.location

    def getPopulation(self):
        return self.population

    def __str__(self):
        return "Location: (%d, %d)" % (self.x, self.y)