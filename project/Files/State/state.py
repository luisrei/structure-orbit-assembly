# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:48:16 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

import bisect

class State:
    """
    Contains a list of the components in orbit 'orbitSet', the date of the state
    'date', the cost associated with the state 'cost' and a list of possible 
    actions that may result in new states 'actions'
    """
    def __init__(self, graph, action, oSet = [], gSet = [], root = True):  
        self.graph = graph
        self.orbitSet = self.updateOrbitSet(action, oSet) # List of names of components in orbit
        self.groundSet = self.updateGroundSet(action, gSet, root)# List of names of components not in orbit
        self.date = action.getDate()   # State date         
        
    def __repr__(self):
        return "<OS %s, Date %s>" % (self.orbitSet, self.date)
        
    def getDate(self):
        return self.date
        
    def initGroundSet(self, graph, gSet):
        "Initializes the list of component not in orbit"
        for v in graph.getVertices():
            gSet.append(v.getName())
        return gSet
        
    def updateGroundSet(self, action, gSet, root):
        "Updates list of components not in orbit"
        if root == True:
            return self.initGroundSet(self.graph, gSet)
        else:
            for v in action.getSet():
                gSet.remove(v)        
            return gSet
    
    def getOrbitSet(self):
        return self.orbitSet
    
    def getGroundSet(self):
        return self.groundSet
    
    def updateOrbitSet(self, action, oSet):
        "Updates list of components in orbit"
        for a in action.set:
            bisect.insort(oSet, a)
        return oSet
            