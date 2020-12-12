"""
AMMM Project
Representation of a problem instance
Eloy Marín, Pablo Pazos
File given Luis Velasco and under its copyright policy
Modified for project purposes
"""

import math

from Heuristics.problem.City import City
from Heuristics.problem.Location import Location
from Heuristics.problem.solution import Solution
from Heuristics.problem.Type import Type

# function that compute the euclidean distance between 2 points
# It is used to check distance constraints
def distance(l1, l2, min_dist=None):
    d = math.sqrt(math.pow(l1.getX() - l2.getX(), 2) + math.pow(l1.getY() - l2.getY(), 2))
    if min_dist is not None:
        return d >= min_dist
    else:
        return d


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        nLocations = inputData.nLocations
        nCities = inputData.nCities
        nTypes = inputData.nTypes

        p = inputData.p
        posCities = inputData.posCities

        posLocations = inputData.posLocations

        d_city = inputData.d_city
        cap = inputData.cap
        cost = inputData.cost

        d_center = inputData.d_center

        # Create Location objects
        self.locations = [None] * nLocations
        for i, location in enumerate(posLocations):
            self.locations[i] = Location(location[0], location[1], i)

        # Create City objects
        self.cities = [None] * nCities
        for i in range(nCities):
            x = posCities[i][0]
            y = posCities[i][1]
            self.cities[i] = City(Location(x, y, i), p[i])

        # Create Type objects
        self.types = [None] * nTypes
        for i in range(nTypes):
            self.types[i] = Type(d_city[i], cap[i], cost[i], i)

        # Get locations that are at distance >= d_center
        self.distance_l1l2 = [None] * nLocations
        for i in range(nLocations):
            self.distance_l1l2[i] = []

        for i in range(nLocations):
            for j in range(nLocations):
                if i != j and distance(self.locations[i], self.locations[j], d_center):
                    self.distance_l1l2[i].append(j)

        # Get distance between locations and cities
        self.distance_cl = [None] * nCities
        for i in range(nCities):
            self.distance_cl[i] = [None] * nLocations

        for i in range(nCities):
            for j in range(nLocations):
                d = distance(self.cities[i].getLocation(), self.locations[j])
                self.distance_cl[i][j] = d

    def getNumLocations(self):
        return len(self.locations)

    def getNumCities(self):
        return len(self.cities)

    def getCities(self):
        return self.cities

    def getLocations(self):
        return self.locations

    def getTypes(self):
        return self.types

    def get_locations_at_min_distance(self):
        return self.distance_l1l2

    def get_cities_locations_distance(self):
        return self.distance_cl

    def createSolution(self):
        solution = Solution(self.cities, self.locations, self.types, self.distance_l1l2, self.distance_cl)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        for v in self.distance_l1l2:
            for j in v:
                if j is not None:
                    return True
        return False
