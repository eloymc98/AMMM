"""
AMMM Project
Representation of a solution
Eloy Marín, Pablo Pazos
File given Luis Velasco and under its copyright policy
Modified for project purposes
"""

import copy
import random

from Heuristics.solution import _Solution


# This class stores the location and center type that serves as primary/secondary center a given city.
class Assignment(object):
    def __init__(self, location, type, city, is_primary, cost=None):
        self.location = location
        self.type = type
        self.city = city
        self.is_primary = is_primary
        if cost is None:
            self.cost = float('infinity')
        else:
            self.cost = cost

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
        # add to this dict locations that are used. key: l_id , value: type class
        self.locations_used = {}
        self.aux_locations_used = {}
        # for each city define its primary and secondary centers
        # {c_id: {'primary': l1_id, 'secondary': l2_id}}
        self.cities_centers = {}
        self.usedPopulationPerCenter = {}
        # key: location_id, value: [(city,primary/secondary)]
        self.cities_served_per_each_location = {}
        self.complete = False

        super().__init__()

    # Update the total cost of the solution
    def update_cost(self, assignment_cost):
        self.cost += assignment_cost

    def get_cost(self):
        return self.cost

    # Check if the solution is completed
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

        # Check if we want to make this location-type primary but distance constraint is not fulfilled
        if pc_or_sc == 'primary' and self.cl_distances[city.getId()][location.getId()] > type.get_d_city():
            return False
        # Check if we want to make this location-type secondary but distance constraint is not fulfilled
        elif pc_or_sc == 'secondary' and self.cl_distances[city.getId()][location.getId()] > 3 * type.get_d_city():
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
            if pc_or_sc == 'primary' and type.get_capacity() - self.usedPopulationPerCenter[location.getId()] < city.getPopulation():
                return False
            elif pc_or_sc == 'secondary' and type.get_capacity() - self.usedPopulationPerCenter[location.getId()] < 0.1 * city.getPopulation():
                return False

        # If we change center type, we have to respect the distances of the cities that it serves as primary/secondary
        # and its capacity
        if self.locations_used.get(location.getId()) is not None:
            old_type = self.locations_used[location.getId()]
            if old_type.get_id() != type.get_id():
                for value in self.cities_served_per_each_location[location.getId()]:
                    if value[1] == 'primary' and self.cl_distances[value[0].getId()][location.getId()] > type.get_d_city():
                        return False
                    elif value[1] == 'secondary' and self.cl_distances[value[0].getId()][location.getId()] > 3 * type.get_d_city():
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

    def get_type_assigned_to_locationId(self, locationId):
        return self.locations_used[locationId]

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
            try:
                self.cities_served_per_each_location[location.getId()].remove((city, pc_or_sc))
            except ValueError:
                index_to_delete = None
                for i, v in enumerate(self.cities_served_per_each_location[location.getId()]):
                    if v[0].getId() == city.getId():
                        index_to_delete = i
                        break
                if index_to_delete is not None:
                    del self.cities_served_per_each_location[location.getId()][index_to_delete]
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

    def change_location_type(self, location, t):
        population = self.usedPopulationPerCenter[location.getId()]
        infeasible = False
        for value in self.cities_served_per_each_location[location.getId()]:
            # Check if new type would respect distance constraints of other cities
            if value[1] == 'primary' and self.cl_distances[value[0].getId()][location.getId()] > t.get_d_city():
                infeasible = True
                break
            elif value[1] == 'secondary' and self.cl_distances[value[0].getId()][location.getId()] > 3 * t.get_d_city():
                infeasible = True
                break

        # Check if new type would have capacity for other served cities
        if t.get_capacity() < population:
            infeasible = True

        if infeasible:
            return False

        assignment_cost = 0
        if self.locations_used[location.getId()].get_id() != t.get_id():
            assignment_cost = t.get_cost() - self.locations_used[location.getId()].get_cost()
            self.locations_used[location.getId()] = t
        self.cost += assignment_cost

        return True

    def findFeasibleAssignments(self):
        feasibleAssignments = []
        for c in self.cities:
            for l in self.locations:
                for t in self.types:
                    for pc_or_sc in ['primary', 'secondary']:
                        feasible = self.assign(c, l, t, pc_or_sc)
                        if not feasible: continue
                        is_primary = True if pc_or_sc == 'primary' else False
                        assignment = Assignment(l, t, c, is_primary)
                        assignment.cost = self.cost
                        feasibleAssignments.append(assignment)

                        self.unassign(c, l, t, pc_or_sc)

        return feasibleAssignments

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
                        if bestAssignment.cost > current_cost or (
                                bestAssignment.cost == current_cost and random.random() > 0.5):
                            bestAssignment.location = l
                            bestAssignment.city = c
                            bestAssignment.type = t
                            bestAssignment.is_primary = True if pc_or_sc == 'primary' else False
                            bestAssignment.cost = self.cost

                        self.unassign(c, l, t, pc_or_sc)

        return bestAssignment

    def __str__(self):
        result_str = f'Solution found with cost {self.cost}\n'
        for k in self.locations_used.keys():
            result_str += f'Location {k} has a center of type {self.locations_used[k].get_id()}.'
            result_str += f' It serves {round(self.usedPopulationPerCenter[k], 2)} inhabitants,'
            result_str += f' max is {self.locations_used[k].get_capacity()}.\n'
        for i in self.cities_centers.keys():
            result_str += f'City {i} primary center is at location {self.cities_centers[i]["primary"]}'
            result_str += f' (distance {self.cl_distances[i][self.cities_centers[i]["primary"]]},'
            result_str += f' max is {self.locations_used[self.cities_centers[i]["primary"]].get_d_city()}).\n'

            result_str += f'City {i} secondary center is at location {self.cities_centers[i]["secondary"]}'
            result_str += f' (distance {self.cl_distances[i][self.cities_centers[i]["secondary"]]},'
            result_str += f' max is {3 * self.locations_used[self.cities_centers[i]["secondary"]].get_d_city()}).\n'

        return result_str

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
