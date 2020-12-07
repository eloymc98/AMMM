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


# This class stores the location and center type that serves as primary/secondary center a given city.
class Assignment(object):
    def __init__(self, location, type, city, is_primary):
        self.location = location
        self.type = type
        self.city = city
        self.is_primary = is_primary
        self.cost = float('infinity')

    def __str__(self):
        return "<c_%d, l_%d, t_%d>: %s center" % (
            self.city.getId(), self.location.getId(), self.type.get_id(), 'Primary' if self.is_primary else 'Secondary')


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, cities, locations, types, compatible_locations, cl_distances):
        self.cost = 0.0
        self.cities = cities
        self.locations = locations
        self.types = types
        self.compatible_locations = compatible_locations
        self.cl_distances = cl_distances

        self.locations_used = {}  # add to this dict locations that are used. key: l_id , value: t_id
        # for each city define its primary and secondary centers
        self.cities_centers = [{'primary': None, 'secondary': None}] * len(self.cities)
        self.loadPerCenter = {}
        self.usedPopulationPerCenter = {}

        super().__init__()

    def update_cost(self, assignment_cost):
        self.cost += assignment_cost

    def isFeasibleToAssignCenterToCity(self, city, location, type, pc_or_sc):

        # Check if location is already used with another type
        # if len(self.locations_used) > 0:
        #     for l in self.locations_used:
        #         if location.getId() == l[0] and type.get_id() != l[1]:
        #             return False

        if self.cities_centers[city.getId()][pc_or_sc] is not None:
            # Check if this city has already been a assigned a primary/secondary center
            return False
        elif pc_or_sc == 'primary' and self.cl_distances[city.getId(), location.getId()] > type.get_d_city():
            # Check if we want to make this location-type primary but distance constraint is not fulfilled
            return False
        elif pc_or_sc == 'secondary' and self.cl_distances[city.getId(), location.getId()] > 3 * type.get_d_city():
            # Check if we want to make this location-type secondary but distance constraint is not fulfilled
            return False

        # Check if location is compatible with locations already used
        if len(self.locations_used) > 0:
            flag = False
            for k in self.locations_used.keys():
                if location.getId() in self.compatible_locations[k]:
                    flag = True
                    break
            if not flag:
                return False

        if pc_or_sc == 'primary' and type.get_capacity() - self.usedPopulationPerCenter[
            location.getId()] < city.getPopulation():
            return False
        elif pc_or_sc == 'secondary' and type.get_capacity() - self.usedPopulationPerCenter[
            location.getId()] < 0.1 * city.getPopulation():
            return False

        return True

    def isFeasibleToUnassignTaskFromCPU(self, taskId, cpuId):
        if taskId not in self.taskIdToCPUId: return False
        if cpuId not in self.cpuIdToListTaskId: return False
        if taskId not in self.cpuIdToListTaskId[cpuId]: return False
        return True

    def getCPUIdAssignedToTaskId(self, taskId):
        if taskId not in self.taskIdToCPUId: return None
        return self.taskIdToCPUId[taskId]

    def assign(self, city, location, type, pc_or_sc):
        if not self.isFeasibleToAssignCenterToCity(city, location, type, pc_or_sc): return False

        assignment_cost = 0
        if self.locations_used.get(location.getId()) is None:
            assignment_cost = type.get_cost()
        elif self.locations_used[location.getId()] != type.get_id():
            assignment_cost = type.get_cost() - self.locations_used[location.getId()].get_cost()

        self.locations_used[location.getId()] = type.get_id()
        self.cities_centers[city.getId()][pc_or_sc] = location.getId()

        population = city.getPopulation() if pc_or_sc == 'primary' else 0.1 * city.getPopulation()
        if self.usedPopulationPerCenter.get(location.getId()) is None:
            self.usedPopulationPerCenter[location.getId()] = population
        else:
            self.usedPopulationPerCenter[location.getId()] += population

        self.cost += assignment_cost
        return True

    def unassign(self, taskId, cpuId):
        if not self.isFeasibleToUnassignTaskFromCPU(taskId, cpuId): return False

        del self.taskIdToCPUId[taskId]
        self.cpuIdToListTaskId[cpuId].remove(taskId)
        self.availCapacityPerCPUId[cpuId] += self.tasks[taskId].getTotalResources()

        self.updateHighestLoad()
        return True

    def findFeasibleAssignments(self):
        feasibleAssignments = []
        for c in self.cities:
            c_id = c.getId()
            for l in self.locations:
                l_id = l.getId()
                feasible = self.assign(c_id, cpuId)
            if not feasible: continue
            assignment = Assignment(taskId, cpuId, self.fitness)
            feasibleAssignments.append(assignment)

            self.unassign(taskId, cpuId)

        return feasibleAssignments

    def findBestFeasibleAssignment(self):
        bestAssignment = Assignment(None, None, None, None)
        for c in self.cities:
            for l in self.locations:
                for t in self.types:
                    for pc_or_sc in ['primary', 'secondary']:
                        feasible = self.assign(c, l, t, pc_or_sc)
                        if not feasible: continue

                        current_cost = self.cost
                        if bestAssignment.cost > current_cost:
                            bestAssignment.location = l
                            bestAssignment.city = c
                            bestAssignment.type = t
                            bestAssignment.is_primary = True if pc_or_sc == 'primary' else False
                            bestAssignment.cost = self.cost

                        self.unassign(taskId, cpuId)

        return bestAssignment

    def __str__(self):
        strSolution = 'z = %10.8f;\n' % self.fitness
        if self.fitness == float('inf'): return strSolution

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
