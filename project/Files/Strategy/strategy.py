# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 11:42:57 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

import bisect

class Queue:
    "Queue is an abstract class/interface"

    def __init__(self):
        raise NotImplementedError

    def extend(self, items):
        for item in items:
            self.append(item)


class Strategy(Queue):
    """
    Returns element based on its cost - evaluated by some function f.
    Order parameter determines if we return element with max/min cost value.
    """
    
    def __init__(self, f, order = min, sm = "u"):
        self.A = [] # Open List
        self.E = [] # Closed List
        self.order = order
        self.f = f
        self.search = sm

    def append(self, item, ok = False):
        "Inserts in Closed List"
        
        inThere  = False

        for e in self.E:    # Check if Node in closed List
            if (item.currState.getDate() == e.currState.getDate()) and (item.currState.getOrbitSet() == e.currState.getOrbitSet()): # If so, Node with smaller cost has already been expanded
                inThere = True
                break
        if inThere == False: # If not, check if node in open List
            for a in self.A:
                if (item.currState.getDate() == a.currState.getDate()) and (item.currState.getOrbitSet() == a.currState.getOrbitSet()):
                    if (item < a):
                        self.A.remove(a)    # Node with smaller cost found => replace in List
                        break
                    else:
                        inThere = True
        if inThere == False: # Either Node with smaller cost has been found or Node not in List
            bisect.insort(self.A, item)
            

    def getSearch(self):
        "Returns search method"
        return self.search

    def appendOL(self, node):
        "Inserts in Open List"
        self.E.append(node)

    def __len__(self):
        return len(self.A)

    def getNextNode(self):
        if self.order == min:
            x = self.A.pop(0)
            return x        
        else:
            return self.A.pop()

    def __contains__(self, item):
        return any(item == pair for pair in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)


