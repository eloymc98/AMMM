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

from Heuristics.problem.Task import Task
from Heuristics.problem.CPU import CPU
from Heuristics.problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        nLocations = inputData.nLocations
        nCities = inputData.nCities
        nTypes = inputData.nTypes
        rt = inputData.rt
        self.rc = inputData.rc

        self.tasks = [None] * nTasks  # vector with tasks
        for tId in range(0, nTasks):  # tId = 0..(nTasks-1)
            self.tasks[tId] = Task(tId, rt[tId])

        self.cpus = [None] * nCPUs  # vector with cpus
        for cId in range(0, nCPUs):  # cId = 0..(nCPUs-1)
            self.cpus[cId] = CPU(cId, self.rc[cId])

    def getNumTasks(self):
        return len(self.tasks)

    def getNumCPUs(self):
        return len(self.cpus)

    def getTasks(self):
        return self.tasks

    def getCPUs(self):
        return self.cpus

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
