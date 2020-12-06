import math


class LogisticCenter(object):
    def __init__(self, id, workingDistanceType):
        self.id = id
        self.type = None
        self.locationAssigned = None
        self.workingDistanceType = workingDistanceType

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def getLocationAssigned(self):
        return self.locationAssigned

    def getWorkingDistanceType(self):
        return self.workingDistanceType

    def setType(self, type):
        self.type = type

    def set_working_distance_type(self, workingDistanceType):
        self.workingDistanceType = workingDistanceType

    def setLocationAssigned(self, locationAssigned):
        self.locationAssigned = locationAssigned

    def isInWorkingDistance(self, locationCity):
        if self.locationAssigned is None:
            return False

        xCity = locationCity.getLocation().getX()
        yCity = locationCity.getLocation().getX()
        xCenter = self.locationAssigned.getX()
        yCenter = self.locationAssigned.getY()

        if self.workingDistanceType == 'Primary':
            return math.sqrt(math.pow(xCity - xCenter, 2) + math.pow(yCity - yCenter, 2)) <= self.getType().get_d_city()
        else:
            return math.sqrt(math.pow(xCity - xCenter, 2) + math.pow(yCity - yCenter, 2)) <= 3 * self.getType().get_d_city()

    def __str__(self):
        return "Center: type %s pos (%d, %d)" % (self.type, self.locationAssigned.getX(), self.locationAssigned.getY())
