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
import random

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

        self.locations_used = {}  # add to this dict locations that are used. key: l_id , value: type class

        self.aux_locations_used = {}
        # for each city define its primary and secondary centers
        self.cities_centers = {}  # {c_id: {'primary': l1_id, 'secondary': l2_id}}
        self.usedPopulationPerCenter = {}
        self.cities_served_per_each_location = {}  # key: location_id, value: [(city,primary/secondary)]
        self.complete = False

        super().__init__()

    def update_cost(self, assignment_cost):
        self.cost += assignment_cost

    def is_complete(self):
        if len(self.cities_centers.keys()) == len(self.cities):
            complete_solution = True
            for key in self.cities_centers.keys():
                if self.cities_centers[key].get('primary') is None or self.cities_centers[key].get('secondary') is None:
                    complete_solution = False
            if complete_solution:
                self.complete = True

    def isFeasibleToAssignCenterToCity(self, city, location, type, pc_or_sc):

        # Check if location is already used with another type
        # if len(self.locations_used) > 0:
        #     for l in self.locations_used:
        #         if location.getId() == l[0] and type.get_id() != l[1]:
        #             return False
        if self.cities_centers.get(city.getId()) is not None:
            if self.cities_centers[city.getId()].get(pc_or_sc) is not None:
                # Check if this city has already been a assigned a primary/secondary center
                return False
            elif pc_or_sc == 'primary' and self.cities_centers[city.getId()].get('primary') is None and \
                    self.cities_centers[city.getId()].get('secondary') == location.getId():
                return False
            elif pc_or_sc == 'secondary' and self.cities_centers[city.getId()].get('secondary') is None and \
                    self.cities_centers[city.getId()].get('primary') == location.getId():
                return False

        if pc_or_sc == 'primary' and self.cl_distances[city.getId()][location.getId()] > type.get_d_city():
            # Check if we want to make this location-type primary but distance constraint is not fulfilled
            return False
        elif pc_or_sc == 'secondary' and self.cl_distances[city.getId()][location.getId()] > 3 * type.get_d_city():
            # Check if we want to make this location-type secondary but distance constraint is not fulfilled
            return False

        # Check if location is compatible with locations already used
        if len(self.locations_used.keys()) > 0:
            flag = True
            for k in self.locations_used.keys():
                if location.getId() not in self.compatible_locations[k]:
                    flag = False
            if location.getId() in self.locations_used.keys():
                flag = True
            if not flag:
                return False

        if self.usedPopulationPerCenter.get(location.getId()) is not None:
            if pc_or_sc == 'primary' and type.get_capacity() - self.usedPopulationPerCenter[
                location.getId()] < city.getPopulation():
                return False
            elif pc_or_sc == 'secondary' and type.get_capacity() - self.usedPopulationPerCenter[
                location.getId()] < 0.1 * city.getPopulation():
                return False

        # If we change center type, we have to respect the distances of the cities that it serves as primary/secondary
        # and its capacity
        if self.locations_used.get(location.getId()) is not None:
            old_type = self.locations_used[location.getId()]
            if old_type.get_id() != type.get_id():
                for value in self.cities_served_per_each_location[location.getId()]:
                    if value[1] == 'primary' and self.cl_distances[value[0].getId()][
                        location.getId()] > type.get_d_city():
                        return False
                    elif value[1] == 'secondary' and self.cl_distances[value[0].getId()][
                        location.getId()] > 3 * type.get_d_city():
                        return False

        return True

    def isFeasibleToUnassignCenterFromCity(self, city, location, type, pc_or_sc):
        if self.locations_used.get(location.getId()) is None:
            return False
        if self.locations_used[location.getId()].get_id() != type.get_id():
            return False
        if self.cities_centers[city.getId()][pc_or_sc] != location.getId():
            return False
        return True

    def getCPUIdAssignedToTaskId(self, taskId):
        if taskId not in self.taskIdToCPUId: return None
        return self.taskIdToCPUId[taskId]

    def assign(self, city, location, type, pc_or_sc, check_completeness=False):
        if not self.isFeasibleToAssignCenterToCity(city, location, type, pc_or_sc): return False

        assignment_cost = 0
        if self.locations_used.get(location.getId()) is None:
            assignment_cost = type.get_cost()
        elif self.locations_used[location.getId()].get_id() != type.get_id():
            assignment_cost = type.get_cost() - self.locations_used[location.getId()].get_cost()
            if not check_completeness:
                self.aux_locations_used[location.getId()] = self.locations_used[location.getId()]

        self.locations_used[location.getId()] = type
        if self.cities_served_per_each_location.get(location.getId()) is None:
            self.cities_served_per_each_location[location.getId()] = []
        self.cities_served_per_each_location[location.getId()].append((city, pc_or_sc))

        if self.cities_centers.get(city.getId()) is not None:
            self.cities_centers[city.getId()][pc_or_sc] = location.getId()
        else:
            self.cities_centers[city.getId()] = {}
            self.cities_centers[city.getId()][pc_or_sc] = location.getId()

        population = city.getPopulation() if pc_or_sc == 'primary' else 0.1 * city.getPopulation()
        if self.usedPopulationPerCenter.get(location.getId()) is None:
            self.usedPopulationPerCenter[location.getId()] = population
        else:
            self.usedPopulationPerCenter[location.getId()] += population

        self.cost += assignment_cost

        if check_completeness:
            self.is_complete()
        return True

    def unassign(self, city, location, type, pc_or_sc):
        if not self.isFeasibleToUnassignCenterFromCity(city, location, type, pc_or_sc): return False

        assignment_cost = 0
        if self.aux_locations_used.get(location.getId()) is not None:
            assignment_cost = self.locations_used[location.getId()].get_cost() - self.aux_locations_used[
                location.getId()].get_cost()
            self.locations_used[location.getId()] = copy.deepcopy(self.aux_locations_used[location.getId()])
            del self.aux_locations_used[location.getId()]
        elif len(self.cities_served_per_each_location[location.getId()]) == 1:
            assignment_cost = self.locations_used[location.getId()].get_cost()
            del self.locations_used[location.getId()]

        if len(self.cities_served_per_each_location[location.getId()]) > 1:
            self.cities_served_per_each_location[location.getId()].remove((city, pc_or_sc))
        else:
            del self.cities_served_per_each_location[location.getId()]

        self.cities_centers[city.getId()][pc_or_sc] = None

        population = city.getPopulation() if pc_or_sc == 'primary' else 0.1 * city.getPopulation()
        if self.usedPopulationPerCenter.get(location.getId()) == population:
            del self.usedPopulationPerCenter[location.getId()]
        else:
            self.usedPopulationPerCenter[location.getId()] -= population

        self.cost -= assignment_cost
        return True

    def findBestFeasibleAssignment(self):
        bestAssignment = Assignment(None, None, None, None)
        for c in self.cities:
            for l in self.locations:
                for t in self.types:
                    for pc_or_sc in ['primary', 'secondary']:
                        if c.getId() in (4, 5, 6) and l.getId() == 0 and pc_or_sc == 'primary':
                            pass

                        feasible = self.assign(c, l, t, pc_or_sc)
                        if not feasible: continue

                        current_cost = self.cost
                        if bestAssignment.cost > current_cost or (bestAssignment.cost == current_cost and random.random() > 0.5):
                            bestAssignment.location = l
                            bestAssignment.city = c
                            bestAssignment.type = t
                            bestAssignment.is_primary = True if pc_or_sc == 'primary' else False
                            bestAssignment.cost = self.cost

                        self.unassign(c, l, t, pc_or_sc)

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
