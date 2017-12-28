# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 11:22:58 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from State.node import Node

def generalSearch(Problem, Strategy):
    if Strategy.getSearch() == "i":
        node = Node(Problem.getInitState(), heuristic = Problem.heuristic(Problem.getInitState().getGroundSet(), Problem.getInitState().getDate()))
    else:
        node = Node(Problem.getInitState())
    Strategy.append(node)
    while Strategy:  # while frontier not empty, continue the search
        node = Strategy.getNextNode()

        if Problem.checkGoal(node):  # check goal condition
            node.solution()
            return None
        
        Strategy.appendOL(node)
        for child in node.expand(Problem, Strategy.getSearch()):  # add child nodes to frontier
            Strategy.append(child)
            
    # No solution was found
    node.noSolution()       
    return None