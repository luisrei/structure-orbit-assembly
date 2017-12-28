# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 19:07:20 2017

Checks if the solver.py function was called correctly

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from Problem.problem import Problem
from Utils.graph import Graph
from informed import informed
from uninformed import uninformed
import sys


def checkArgs(args):
    "Checks input arguments validity"
    if (len(args) != 3) or not((args[1] == "-u" or args[1] == "-i")):
        return False
    
    return True
        

# MAIN                    
if __name__ == "__main__":
    "Solves search problem"
    
    # Checks proper usage
    if not checkArgs(sys.argv):
        print("Usage: solver.py search_method filename" + "\n 'search_method' field must be either '-u' or '-i' for uninformed and informed search respectively\n")
        sys.exit(1)
    else:
        
        try:
            # Initializes a graph representing the state
            g = Graph(sys.argv[2])
        except IOError:
            print("Error: Could not read file!")
            sys.exit(1)
        except RuntimeError:
            print("Error: File not in an acceptable format!")
            sys.exit(1)
        
        # Initializes problem structure with initial state, successor and cost function
        # Initializes actions available
        prob = Problem(g)
        
        # Calls for specified search algorithm to be run
        if sys.argv[1] == "-u":
            result = uninformed(prob)
        elif sys.argv[1] == "-i":
            result = informed(prob)                