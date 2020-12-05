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

from Heuristics.problem.LogisticCenter import LogisticCenter
from Heuristics.problem.City import City
from Heuristics.problem.Location import Location
from Heuristics.problem.solution import Solution
from Heuristics.problem.Type import Type


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

        self.d_center = inputData.d_center

        self.locations = [None] * nLocations
        for i, location in enumerate(posLocations):
            self.locations[i] = Location(location[0], location[1])

        self.cities = [None] * nCities
        for i in range(posCities):
            x = posCities[i][0]
            y = posCities[i][1]
            self.cities[i] = City(Location(x, y), p[i])

        self.types = [None] * nTypes
        for i in range(nTypes):
            self.types[i] = Type(d_city[i], cap[i], cost[i])

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

    def createSolution(self):
        solution = Solution(self.tasks, self.cpus, self.rc)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        totalCapacityCPUs = 0.0
        maxCPUCapacity = 0.0
        for cpu in self.cpus:
            capacity = cpu.getTotalCapacity()
            totalCapacityCPUs += capacity
            maxCPUCapacity = max(maxCPUCapacity, capacity)

        totalResourcesTasks = 0.0
        for task in self.tasks:
            resources = task.getTotalResources()
            totalResourcesTasks += resources
            if resources > maxCPUCapacity: return False

        return totalCapacityCPUs >= totalResourcesTasks