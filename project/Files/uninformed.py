# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 13:30:49 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from Strategy.strategy import Strategy
from Search.general import generalSearch

def uninformed(problem):
    
    # Initializes strategy
    strat = Strategy(lambda node: node.getPathCost(), min)

    # Runs general search algorithm with domain dependent parameters
    generalSearch(problem, strat)
    