"""
AMMM Lab Heuristics
Representation of a solution instance
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

import copy
from Heuristics.solution import _Solution
from Heuristics.problem.LogisticCenter import LogisticCenter


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, location, type, city):
        self.location = location
        self.type = type
        self.city = city

    def __str__(self):
        return "<(%d, %d), %s, ((%d, %d), %d)>: highestLoad: %.2f%%" % (self.location.getX(),
                                                                        self.location.getY(),
                                                                        self.type,
                                                                        self.city.getLocation().getX(),
                                                                        self.city.getLocation().getY(),
                                                                        self.city.getPopulation())


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, cities, locations, types, compatible_locations, cl_distances, centers):
        self.cost = 0.0
        self.cities = cities
        self.centers = centers
        self.locations = locations
        self.types = types
        self.compatible_locations = compatible_locations
        self.cl_distances = cl_distances
        self.locations_used = []  # add to this list locations that are used
        self.location_used_to_center_type = {}  # location Id -> center type Id
        self.loadPerCenter = []
        self.availablePopulationPerCenter = []
        # for each city define its primary and secondary centers
        self.cities_centers = [{'primary': None, 'secondary': None}] * len(self.cities)

        super().__init__()

    def updateHighestLoad(self):
        for center in self.centers:
            centerId = center.getId()
            totalPopulation = center.getMaxCap()
            usedPopulation = totalPopulation - self.availablePopulationPerCenter[centerId]
            load = usedPopulation / totalPopulation
            self.loadPerCenter[centerId] = load
            self.cost += center.getInstallationCost()

    def isFeasibleToAssignLocationCenter(self, center, city):
        if center.getMaxCap() < self.availablePopulationPerCenter[center.getId()] + city.getPopulation():
            return False
        return center.isInWorkingDistance(city)

    def isFeasibleToUnassignLocationCenter(self, center, city):
        if center.getLocation() not in self.locations_used: return False
        return True

    def assign(self, center, city):
        if not self.isFeasibleToAssignLocationCenter(center, city): return False

        centerId = center.getId()
        cityId = city.getId()
        self.locations_used[centerId] = center.getLocation()
        self.location_used_to_center_type[center.getLocation] = center.getType()
        self.cities_centers[cityId] = center.getType()
        self.availablePopulationPerCenter[centerId] -= city.getPopulation()

        self.updateHighestLoad()
        return True

    def unassign(self, center, city):
        if not self.isFeasibleToUnassignLocationCenter(center, city): return False

        centerId = center.getId()
        cityId = city.getId()
        del self.locations_used[centerId]
        del self.location_used_to_center_type[center.getLocation]
        del self.cities_centers[cityId]
        self.availablePopulationPerCenter[centerId] += city.getPopulation()

        self.updateHighestLoad()
        return True

    def findFeasibleAssignments(self, city):
        feasibleAssignments = []
        for location in self.locations:
            if location in self.locations_used: continue
            else:
                for center in self.centers:
                    if center.getLocation() is not None: continue
                    else:
                        center.setLocationAssigned(location)
                        center.setType('primary')
                        feasible = self.assign(center, city)
                        if feasible is False: center.setType('secondary')
                        feasible = self.assign(center, city)
                        if not feasible: continue
                        else:
                            assignment = Assignment(center.getLocation(), center.getType(), city)
                            feasibleAssignments.append(assignment)

                    self.unassign(center, city)

        return feasibleAssignments

    def findBestFeasibleAssignment(self, center, city):
        bestAssignment = Assignment(center.getLocation(), center.getType(), city)
        best_cost = float('infinity')
        for location in self.locations:
            if location in self.locations_used: continue
            else:
                for center in self.centers:
                    if center.getLocation() is not None: continue
                    center.setLocationAssigned(location)
                    center.setType('primary')
                    feasible = self.assign(center, city)
                    if feasible is False: center.setType('secondary')
                    feasible = self.assign(center, city)
                    if not feasible: continue

                    actual_cost = center.getInstallationCost()
                    if actual_cost > best_cost:
                        bestAssignment.location = center.location
                        best_cost = actual_cost

            self.unassign(center, city)

        return bestAssignment

    def __str__(self):
        strSolution = 'z = %10.8f;\n' % self.cost
        if self.cost == float('inf'): return strSolution

        # Xtc: decision variable containing the assignment of tasks to CPUs
        # pre-fill with no assignments (all-zeros)
        xtc = []
        for t in range(0, len(self.tasks)):  # t = 0..(nTasks-1)
            xtcEntry = [0] * len(self.cpus)  # results in a vector of 0's with nCPUs elements
            xtc.append(xtcEntry)

        # iterate over hash table taskIdToCPUId and fill in xtc
        for taskId, cpuId in self.taskIdToCPUId.items():
            xtc[taskId][cpuId] = 1

        strSolution += 'xtc = [\n'
        for xtcEntry in xtc:
            strSolution += '\t[ '
            for xtcValue in xtcEntry:
                strSolution += str(xtcValue) + ' '
            strSolution += ']\n'
        strSolution += '];\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
