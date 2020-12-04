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


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, taskId, cpuId, highestLoad):
        self.taskId = taskId
        self.cpuId = cpuId
        self.highestLoad = highestLoad

    def __str__(self):
        return "<t_%d, c_%d>: highestLoad: %.2f%%" % (self.taskId, self.cpuId, self.highestLoad*100)


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, tasks, cpus, capacityPerCPUId):
        self.tasks = tasks
        self.cpus = cpus
        self.taskIdToCPUId = {}  # hash table: task Id => CPU Id
        self.cpuIdToListTaskId = {}  # hash table: CPU Id => list<task Id>
        # vector of available capacities per CPU initialized as a copy of maxCapacityPerCPUId vector.
        self.availCapacityPerCPUId = copy.deepcopy(capacityPerCPUId)
        # vector of loads per CPU (nCPUs entries initialized to 0.0) 
        self.loadPerCPUId = [0.0] * len(cpus)
        super().__init__()

    def updateHighestLoad(self):
        self.fitness = 0.0
        for cpu in self.cpus:
            cpuId = cpu.getId()
            totalCapacity = cpu.getTotalCapacity()
            usedCapacity = totalCapacity - self.availCapacityPerCPUId[cpuId]
            load = usedCapacity / totalCapacity
            self.loadPerCPUId[cpuId] = load
            self.fitness = max(self.fitness, load)

    def isFeasibleToAssignTaskToCPU(self, taskId, cpuId):
        if taskId in self.taskIdToCPUId:
            return False

        if self.availCapacityPerCPUId[cpuId] < self.tasks[taskId].getTotalResources():
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

    def assign(self, taskId, cpuId):
        if not self.isFeasibleToAssignTaskToCPU(taskId, cpuId):return False

        self.taskIdToCPUId[taskId] = cpuId
        if cpuId not in self.cpuIdToListTaskId: self.cpuIdToListTaskId[cpuId] = []
        self.cpuIdToListTaskId[cpuId].append(taskId)
        self.availCapacityPerCPUId[cpuId] -= self.tasks[taskId].getTotalResources()

        self.updateHighestLoad()
        return True

    def unassign(self, taskId, cpuId):
        if not self.isFeasibleToUnassignTaskFromCPU(taskId, cpuId): return False

        del self.taskIdToCPUId[taskId]
        self.cpuIdToListTaskId[cpuId].remove(taskId)
        self.availCapacityPerCPUId[cpuId] += self.tasks[taskId].getTotalResources()

        self.updateHighestLoad()
        return True

    def findFeasibleAssignments(self, taskId):
        feasibleAssignments = []
        for cpu in self.cpus:
            cpuId = cpu.getId()
            feasible = self.assign(taskId, cpuId)
            if not feasible: continue
            assignment = Assignment(taskId, cpuId, self.fitness)
            feasibleAssignments.append(assignment)

            self.unassign(taskId, cpuId)

        return feasibleAssignments

    def findBestFeasibleAssignment(self, taskId):
        bestAssignment = Assignment(taskId, None, float('infinity'))
        for cpu in self.cpus:
            cpuId = cpu.getId()
            feasible = self.assign(taskId, cpuId)
            if not feasible: continue

            curHighestLoad = self.fitness
            if bestAssignment.highestLoad > curHighestLoad:
                bestAssignment.cpuId = cpuId
                bestAssignment.highestLoad = curHighestLoad

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
