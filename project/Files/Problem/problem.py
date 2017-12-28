# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:18:09 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

import copy, bisect
from State.state import State
from Operator.operator import Action
            
class Problem:
    """
    Contains the initial state of the problem 'initState', the current state being
    expanded 'currState' and the next states being evaluated 'nextState'
    """
    
    def __init__(self, graph):
        self.graph = graph
        self.dict = {}
        self.initState = State(graph, Action([]))
        self.currState = self.initState
        self.nextState = []
        self.dateCosts = self.initHfunction()
            
    def succ(self, state, action):
        "Creates successor state"
        newGSet = copy.copy(state.getGroundSet())
        newOSet = copy.copy(state.getOrbitSet())
        x = State(self.graph, action, newOSet, newGSet, False)
        return x
    
    def cost(self, action): 
        "Computes the cost in accordance to what was said in the project's assignment "
        if len(action.getSet()) == 0:
            return 0
        for l in self.graph.getLaunches():
            if l.getDate() == action.getDate(): # Gets the fixed and unit costs of the launch
                fixedCost = l.getFixedCost()
                unitCost = 0
                
                for var in action.getSet():
                    for v in self.graph.getVertices():
                        if v.getName() == var:
                            price = v.getWeight() * l.getUnitCost() 
                            unitCost = unitCost + price
                finalCost = unitCost + fixedCost
                
                return finalCost          
        
    def initHfunction(self):
        "Initializes the heuristic function"
        h = []
        for l in self.graph.getLaunches():  # Sorted unit cost list
            bisect.insort(h, [l.getDate(), l.getUnitCost()])
            stop = 0
            for i in h[:len(h)-1]:  # Run through the list
                stop = stop + 1
                if i[1]>h[stop][1]: # Lower cost found
                    start = 0
                    while start < stop: # Start updating from the beginning
                        if h[start][1] > h[stop][1]: # If cost at an earlier date is bigger than the one found
                            h[start][1] = h[stop][1]
                        start = start + 1
        return h
        
                
    def heuristic(self, gSet, d):
        "Returns heuristic value of a Node"
        
        w = 0
        for t in self.dateCosts:
            if t[0] > d:
                # Found lowest cost according to my date
                for c in gSet:   # Get component's weight
                    for v in self.graph.getVertices():
                        if c == v.getName():
                            w = w + v.getWeight()*t[1]
                return w
        for c in gSet:   # Get component's weight
            for v in self.graph.getVertices():
                if c == v.getName():
                    w = w + v.getWeight()*self.dateCosts[len(self.dateCosts)-1][1]

        return w
            
                            
    def checkGoal(self, node):
        "Checks if there is no component on the ground"
        if node.getGroundSet() == []:
            return True
        else:
            return False
    
    def getInitState(self):
        "Returns initial state of the problem"
        return self.initState