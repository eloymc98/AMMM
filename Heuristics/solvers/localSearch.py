"""
AMMM Project
Local Search Algorithm
Eloy Marín, Pablo Pazos
File given Luis Velasco and under its copyright policy
Modified for project purposes
"""

import copy
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException


# This class is used to perform sets of modifications.
# A new solution can be created based on an existing solution and a list of
# changes using the createNeighborSolution(solution, moves) function.
class Move(object):
    def __init__(self, c, pc_or_sc, old_l, new_l):  # TODO: Change parameters function
        self.old_l = old_l
        self.c = c
        self.new_l = new_l
        self.pc_or_sc = pc_or_sc

    def __str__(self):
        return f'City {self.c.getId()} {self.pc_or_sc}: Location {self.old_l.getId()} -> Location {self.new_l.getId()}'


# Implementation of a local search using two neighborhoods and oen policy.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def createNeighborSolution(self, solution, moves,old_l_new_t):
        newSolution = copy.deepcopy(solution)

        for move in moves:
            newSolution.unassign(move.c, move.old_l, solution.locations_used[move.old_l.getId()], move.pc_or_sc)

        for move in moves:
            feasible = newSolution.assign(move.c, move.new_l, solution.locations_used[move.new_l.getId()],
                                          move.pc_or_sc)
            if old_l_new_t is not None:
                feasible = newSolution.change_location_type(move.old_l, old_l_new_t)
            if not feasible: return None

        return newSolution

    def get_best_feasible_type(self, solution, city, old_location):
        feasible_types = []
        for t in solution.types:
            population = 0
            infeasible = False
            for value in solution.cities_served_per_each_location[old_location.getId()]:
                if value[0].getId() == city.getId(): continue

                # Check if new type would respect distance constraints of other cities
                if value[1] == 'primary' and solution.cl_distances[value[0].getId()][
                    old_location.getId()] > t.get_d_city():
                    infeasible = True
                    break
                elif value[1] == 'secondary' and solution.cl_distances[value[0].getId()][
                    old_location.getId()] > 3 * t.get_d_city():
                    infeasible = True
                    break

                if value[1] == 'primary':
                    population += value[0].getPopulation()
                elif value[1] == 'secondary':
                    population += 0.1 * value[0].getPopulation()

            # Check if new type would have capacity for other served cities
            if t.get_capacity() < population:
                infeasible = True

            if not infeasible:
                feasible_types.append(t)

        sorted_feasible_types = sorted(feasible_types, key=lambda x: x.get_cost())

        return sorted_feasible_types[0]

    def evaluateNeighbor(self, solution, moves):
        assignment_cost = copy.deepcopy(solution.cost)

        for move in moves:
            city = move.c
            pc_or_sc = move.pc_or_sc
            old_location = move.old_l
            new_location = move.new_l

            if len(solution.cities_served_per_each_location[old_location.getId()]) == 1:
                # If old location only served this city, we can delete it
                assignment_cost -= solution.locations_used[old_location.getId()].get_cost()
            else:
                # If old location type can be changed for another one with lower cost, compute
                # new cost
                new_type = self.get_best_feasible_type(solution, city, old_location)
                assignment_cost += new_type.get_cost() - solution.locations_used[old_location.getId()].get_cost()
                if new_type.get_cost() - solution.locations_used[old_location.getId()].get_cost() != 0:
                    return assignment_cost, new_type

        return assignment_cost, None

    def getCPUswithAssignemnts(self, solution):
        tasks = solution.tasks
        cpus = solution.cpus

        # create vector of assignments <task, cpu>
        cpusWithAssignments = []
        for cpu in cpus:
            cpuId = cpu.getId()
            load = solution.loadPerCPUId[cpuId]
            assignedTasks = solution.cpuIdToListTaskId[cpuId]
            if assignedTasks is None: assignedTasks = []
            assignedTasksWithResources = []
            for taskId in assignedTasks:
                taskPair = (taskId, tasks[taskId].getTotalResources())
                assignedTasksWithResources.append(taskPair)
            assignedTasksWithResources.sort(key=lambda task: task[1], reverse=True)
            cpuWithAssignments = (cpuId, load, solution.availCapacityPerCPUId[cpuId], assignedTasksWithResources)
            cpusWithAssignments.append(cpuWithAssignments)

        # Sort assignments by the load of the assigned CPU in descending order.
        cpusWithAssignments.sort(key=lambda cpuWithAssignment: cpuWithAssignment[1], reverse=True)
        return cpusWithAssignments

    def getLocationAssignmentsSortedByCost(self, solution):
        locations_used = solution.locations_used
        locations = solution.locations

        # create vector of assignments <location, type>
        assignments = []
        for l_id in locations_used.keys():
            t = locations_used[l_id]
            l = locations[l_id]
            load = float(solution.usedPopulationPerCenter[l_id] / t.get_capacity())
            assignment = (l, t, t.get_cost(), load)
            assignments.append(assignment)

        # For best improvement policy it does not make sense to sort the locations since all of them must be explored.
        # However, for first improvement, we can start by the tasks assigned to the more loaded CPUs.
        if self.policy == 'BestImprovement':
            return assignments

        # Sort assignments by the load of the assigned CPU in descending order.
        sorted_assignments = sorted(assignments, key=lambda x: x[2], reverse=True)
        return sorted_assignments

    def reassignment_is_feasible(self, solution, city, pc_or_sc, new_location):
        # If new location already serves the city, is not feasible
        if pc_or_sc == 'primary' and solution.cities_centers[city.getId()]['secondary'] == new_location.getId():
            return False
        elif pc_or_sc == 'secondary' and solution.cities_centers[city.getId()]['primary'] == new_location.getId():
            return False

        type = solution.locations_used[new_location.getId()]
        if pc_or_sc == 'primary' and solution.cl_distances[city.getId()][new_location.getId()] > type.get_d_city():
            # Check if we want to make this location-type primary but distance constraint is not fulfilled
            return False
        elif pc_or_sc == 'secondary' and solution.cl_distances[city.getId()][
            new_location.getId()] > 3 * type.get_d_city():
            # Check if we want to make this location-type secondary but distance constraint is not fulfilled
            return False

        # Check if population can fit in new location
        if pc_or_sc == 'primary' and type.get_capacity() - solution.usedPopulationPerCenter[
            new_location.getId()] < city.getPopulation():
            return False
        elif pc_or_sc == 'secondary' and type.get_capacity() - solution.usedPopulationPerCenter[
            new_location.getId()] < 0.1 * city.getPopulation():
            return False

        return True

    def exploreReassignment(self, solution):
        cities_served_per_each_location = solution.cities_served_per_each_location

        current_cost = solution.get_cost()
        bestNeighbor = solution

        sortedAssignments = self.getLocationAssignmentsSortedByCost(solution)

        nLocationsUsed = len(sortedAssignments)

        for i in range(0, nLocationsUsed - 1):
            location = sortedAssignments[i][0]
            for v in cities_served_per_each_location[location.getId()]:
                for j in range(1, nLocationsUsed):
                    if i == j: continue
                    new_location = sortedAssignments[j][0]
                    if self.reassignment_is_feasible(solution, v[0], v[1], new_location):
                        moves = [Move(v[0], v[1], location, new_location)]
                        neighbor_cost, old_l_new_t = self.evaluateNeighbor(solution, moves)
                        if neighbor_cost < current_cost:
                            neighbor = self.createNeighborSolution(solution, moves,old_l_new_t)
                            if neighbor is None: continue
                            if self.policy == 'FirstImprovement':
                                return neighbor
                            else:
                                bestNeighbor = neighbor
                                current_cost = neighbor_cost

        return bestNeighbor

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'Reassignment':
            return self.exploreReassignment(solution)
        else:
            raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible():
            return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentFitness = incumbent.cost
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None:
                break
            neighborFitness = neighbor.cost
            if incumbentFitness <= neighborFitness:
                break
            incumbent = neighbor
            incumbentFitness = neighborFitness

        return incumbent
