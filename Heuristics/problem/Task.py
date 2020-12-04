"""
AMMM Lab Heuristics
Representation of a Task
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


class Task(object):
    def __init__(self, taskId, totalResources):
        self._taskId = taskId
        self._totalResources = totalResources
        self.gene = 1

    def getId(self):
        return self._taskId

    def getTotalResources(self):
        return self._totalResources

    def getWeightedResources(self):
        return self._totalResources * self.gene

    def __str__(self):
        return "_taskId: %d (resources: %f)" % (self._taskId, self._totalResources)
