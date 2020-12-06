"""
AMMM Lab Heuristics
Representation of a problem instance
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import math
from Heuristics.problem.City import City
from Heuristics.problem.Location import Location
from Heuristics.problem.solution import Solution
from Heuristics.problem.Type import Type


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

        self.locations = [None] * nLocations
        for i, location in enumerate(posLocations):
            self.locations[i] = Location(location[0], location[1])

        self.cities = [None] * nCities
        for i in range(nCities):
            x = posCities[i][0]
            y = posCities[i][1]
            self.cities[i] = City(i, Location(x, y), p[i])

        self.types = [None] * nTypes
        for i in range(nTypes):
            self.types[i] = Type(d_city[i], cap[i], cost[i])

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
        # TODO: implement if necessary
        return True
