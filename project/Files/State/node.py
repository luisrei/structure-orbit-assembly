# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 18:27:11 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

import copy, sys
from itertools import count
from datetime import date
from Operator.operator import Action

class Node:
    "A node in our search tree, that we use for our search algorithm"
    
    _ids = count(0)
    def __init__(self, state, parent=None, action=None, pathCost=0, date = date(1,1,1), DICT = {}, heuristic=0):
    # Create a search tree Node, derived from a parent by an action.  
        self.currState = state
        self.dict = DICT
        self.parent = parent
        self.action = action
        self.actions = None # List of possible actions
        self.pathCost = pathCost
        self.heuristic = heuristic
        self.depth = 0
        self.nodeNb = next(self._ids)
        if parent:
            self.depth = parent.depth + 1
        if self.heuristic < 0:
            self.totalCost = sys.maxsize
        else:
            self.totalCost = self.pathCost + self.heuristic
 
    
    def __repr__(self):
        return "<Tc %s Node %s g %s h %s>" % (self.totalCost, self.currState, self.pathCost, self.heuristic)
 
    def __lt__(self, node):  
        "compare nodes by path cost"
        return [self.totalCost, self.heuristic] < [node.totalCost, node.heuristic]
 
    def getDict(self):
        "Returns dictionary"
        return self.dict
    
    def newEntry(self, key, value):
        "Puts a new value in the dictionary with the key 'key'"
        self.dict[key] = value
        
    def getEntry(self, key):
        "Returns value for key 'key'"
        return self.dict[key]
    
    def isInDict(self, key):
        "Checks if there is a value in dict for 'key'"
        return (key in self.dict)
    
    def expand(self, Problem, searchMethod):  
        "Return reachable nodes from the actions possible"

        return [self.childNode(Problem, action, searchMethod)
                for action in self.getActions(self.currState.getOrbitSet(), self.currState.getDate())]

    def childNode(self, Problem, action, searchMethod):  
        "Return Node reachable from a certain action "

        next = Problem.succ(self.currState, action)

        for l in self.currState.graph.getLaunches():
            if l.getDate() == action.getDate():
                pc = self.pathCost + Problem.cost(action)
                h = Problem.heuristic(next.getGroundSet(), l.getDate())
                if searchMethod == "i":
                    return Node(next, self, action, pc, next.date, self.dict, h)
                else:
                    return Node(next, self, action, pc, next.date, self.dict)
 
    def noSolution(self):
        "Print in case of no solution found"
        
        print('0\n\nProgram will now exit.')  
        
    def solution(self): 
        "Return all the actions and path_costs to get to the goal state"
        
        solution = []
        prevCost = 0
        b = pow(self.nodeNb, 1/(self.depth))
        bf = 0
        for i in range(self.depth + 1):
            bf = bf + pow(b, i)
        print("-----------------------------------------------------------------------------\nSolution: %s nodes created, Depth = %d, Branching factor = %f   \n-----------------------------------------------------------------------------" % (self.nodeNb, self.depth, bf))
        for node in self.path()[1:]:
            s = self.printNode(node.action, node.pathCost - prevCost)
            if not s == None:
                print(s)
            prevCost = node.pathCost
        print('{0:.6f}'.format(self.pathCost), "\n\nProgram will now exit.")
        return solution
 
    def printNode(self, action, value):
        "Prints node information"
        if value != 0:
            s = action.getWrittenDate() + "   " + ' '.join(action.getSet()) + "   " + '{0:.6f}'.format(value)
            return s
        return None
    
    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, pathBack = self, []
        while node:
            pathBack.append(node)
            node = node.parent
        return list(reversed(pathBack))
    
    def getGroundSet(self):
        "Returns the current state's ground set"
        return self.currState.getGroundSet()
    
    def getPathCost(self):
        return self.pathCost
    
    def getHeuristic(self):
        return self.heuristic
 
    def __eq__(self, other):
        return isinstance(other, Node) and self.currState == other.currState
 
    def __hash__(self):
        return hash(self.currState)
    
    def getActions(self, Set, Date = date(1,1,1)):
        "Retrieve possible actions"
    
        Operators = []
        d, threshold = self.getEarliestDate(Date)
        if d == date.max:
            return Operators
        actionSet = self.calcActions(Set, threshold) # List of lists

        for a in actionSet: # For each list in actionSet
            x  = Action(a)
            x.setDate(d) 
            Operators.append(x)
            
        Op = self.getTuple(Operators)
        oSet = self.getTuple(Set, False)
        self.newEntry(oSet,  Op)

        return Operators
        
    def getEarliestDate(self, Date = date(1,1,1)):
        "Gets earliest launch date possible"
        tempDate = date.max
        d = date.max
        threshold = 0
        for l in self.currState.graph.getLaunches(): 

            if l.t > Date and l.t < tempDate:
                tempDate = l.t
                threshold = l.getPayload()

        if not tempDate == date.max:
            d = copy.deepcopy(tempDate)
        return d, threshold
    
    def checkActions(self, orbitSet):
        "Check if action set has already been computed"
        oSet = self.getTuple(orbitSet, False)
        if oSet == ():
            oSet = "Empty"
        self.getDict()
        if self.isInDict(oSet):   # Checks if oSet is a key in pb.dict
            return self.tupleToAction(self.getEntry(oSet))
        return None
    
    def tupleToAction(self, Tuple):
        "Turns a tuple into an Action (Tuple must have (date.isoformat(), vertices) as format)"
        act = []    
        for x in Tuple:
            a = Action(list(x))
            d, threshold = self.getEarliestDate(self.currState.getDate())
            if d == date.max:
                return []
            a.setDate(d)
            act.append(a)
        return act
    
    def getTuple(self, List, listOfLists = True):
        "Converts list into tuple"
        if listOfLists == True:
            return tuple(tuple(x.getSet()) for x in List)
        return tuple(List)
    
    def calcActions(self, Set, threshold):  
        "Computes all actions available given a set of components"
        coreList, parentList = self.getCoreActions(Set)
        i = 1
        actions = [[]]
        vc = []
        parents = copy.deepcopy(parentList)
        for c in coreList:  # Gets all chains of components starting at 'c'
            for v in self.currState.graph.getVertices():
                if c == v.getName():
                    t = v.getWeight() 
            if t <= threshold:
                t = threshold - t # Updates threshold
                actions.insert(i, [c])
                i = i + 1
                succList = self.checkAllSucc(c, threshold, Set, vc) # Gets list of successors

                i = self.addToList(actions, succList, i)
                vc.append(c)
            else:
                self.alterParentsList(c, parents)

        self.removeParentsList(parents)
        self.fillMissingActions(actions, parents, threshold)

        return actions
    
    def getCoreActions(self, Set):
        """
        Gets all the direct connections of a set and the parents that have 
        more than one child
        """
        coreActions = []
        parents = []
        if Set == []:   # If set is empty return every component
            for v in self.currState.graph.getVertices():
                coreActions.append(v.getName())
        else:           # Else, return list of components with direct connection to set

            for n in Set:
                children = self.getChildren(n, Set)
                if len(children) > 0:
                    parents.append([n, children])
                for c in children:
                    coreActions.append(c)

        return coreActions, parents
    
    def checkAllSucc(self, comp, threshold, Set = [], vc = []):
        """
        Runs through the State components 'comp' to check their children and all 
        possible combinations of chains
        """
        for v in self.currState.graph.getVertices():
            if comp == v.getName():
                succList = []
                if v.getWeight() <= threshold:   # Check if component fits in launch
                    s = copy.copy(Set)
                    s.append(comp)                  
                    newThreshold = threshold - v.getWeight() # Update chain threshold
                    children = self.getChildren(comp, s)
                    for c in children:  # For every new component added check further links
                        if c not in vc:     # Check if child already in list
                            for x in self.currState.graph.getVertices():
                                if c == x.getName():
                                    if x.getWeight() <= newThreshold:
                                        succList.append([c])
                        newEntry = self.checkAllSucc(c, newThreshold, s, vc)
                        if not newEntry == []:
                            for e in newEntry:
                                succList.append(e)
                    succList = self.chainCombination(succList, newThreshold)
                    for n in succList:  # Update chain of components with fathers of chain
                        n.insert(0, comp)
                return succList
        return succList
            
    def getChildren(self, comp, Set):
        """
        Returns the children of 'comp'(components connected to 'comp' that aren't 
        in the set)
        """
        links = self.currState.graph.getConnections(comp)   # Component connections
        if len(Set) < 2:    # All comps. are children (empty set or 'comp' is set)
            return links
        else:               # Gets rid of components already in the set
            children = []
            for l in links:
                if l not in Set:
                    children.append(l)
            return children
        
    def chainCombination(self, List, threshold):
        """
        Given a list of chains of nodes and its children returns all combinations
        of chains that have cost below the threshold input
        """
        combinations = List
        place = 0
        end = len(List)
        for c in List:      # Runs through all possible actions
            place = place + 1
            for n in range(place, end): # Compares with other actions
                d = c[:]    # 'd' is a copy of 'c'

                if (self.isIn(c, List[n]) == False) and (self.currState.graph.getTotalWeight(c) + self.currState.graph.getTotalWeight(List[n]) <= threshold): # Checks if action is acceptable
                    d.extend(List[n])                  
                    combinations.append(c + List[n])

        return combinations    
    
    def isIn(self, list1, list2):
        "Checks if elements of list1 are in list2"
        for l in list1:
            if l in list2:
                return True
        return False

    
    def fillMissingActions(self, actionList, parentList, threshold):
        "Fills action list with mixes of chains with the same parent or parents in the same set"
        if len(parentList) > 0:
            start = 1
            listToAdd = []      # Final list
            listOfLists = []    # Temporary list
            for p in parentList:    # Check if there are actions with the same parent
                for l in p[1]:                    
                    tempList = []
                    for a in actionList[start:]:
                        if a[0] == l:
                            tempList.append(a)
                            start = start + 1
                    for t in tempList:
                        listOfLists.append(t)
                    for newAddition in self.chainCombination(listOfLists, threshold):
                        if newAddition not in actionList:
                            listToAdd.append(newAddition)
            for al in listToAdd:
                actionList.append(al)
                    
    def alterParentsList(self, comp, List):
        "Alters parent List"
        for l in List:
            if comp in l[1]:
                l[1].remove(comp)
                break
    
    def removeParentsList(self, parents):
        "Removes Parents List if no nodes in Set connecting the children in tempCL"
        if (len(parents) > 0) and (len(parents) < 2):
            if len(parents[0][1]) < 2:
                parents.remove(parents[0])
    
    def addToList(self, list1, list2, index):
        "Puts the elements in 'list2' inside 'list1', starting in position 'index'"
        for l in list2:
            list1.insert(index, l)
            index = index + 1
        return index