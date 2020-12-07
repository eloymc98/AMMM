import math


class LogisticCenter(object):
    def __init__(self, location, type):
        self.location = location
        self.type = type
        self.cities_assigned =

    def getType(self):
        return self.type

    def getMaxCap(self):
        return self.type.get_capacity()

    def getLocationAssigned(self):
        return self.locationAssigned

    def getWorkingDistance(self):
        return self.workingDistance

    def getInstallationCost(self):
        return self.installationCost

    def setType(self, type):
        self.type = type

    def setLocationAssigned(self, locationAssigned):
        self.locationAssigned = locationAssigned

    def isInWorkingDistance(self, locationCity):
        if self.locationAssigned == None:
            return False

        xCity = locationCity.getX()
        yCity = locationCity.getY()
        xCenter = self.locationAssigned.getX()
        yCenter = self.locationAssigned.getY()

        if self.type == 'Primary':
            return math.sqrt(math.pow(xCity - xCenter, 2) + math.pow(yCity - yCenter, 2)) <= self.workingDistance
        else:
            return math.sqrt(math.pow(xCity - xCenter, 2) + math.pow(yCity - yCenter, 2)) <= 3 * self.workingDistance

    def __str__(self):
        return "Center: type %s pos (%d, %d)" % (self.type, self.locationAssigned.getX(), self.locationAssigned.getY())
