# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:15:56 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from Utils.utils import Edge, Vertex, Launch
import re
    
class Graph:
    "Contains a list of all the edges, vertices and launches"
    
    def __init__(self, file):   
        self.edges = list("E")              # List of edges
        self.vertices = list("V")           # List of vertices
        self.launches = list("L")           # List of launches
    
        # Fills graph with necessary nodes and paths
        try:
            with open(file) as fh: #with this we can close the file even if we failed to read it
                text = fh.readlines()
                for line in text:
                    wordList = re.sub("[^\S]", " ",  line).split()  # transforms phrase into list of words
                    if len(wordList) > 1:
                        if "E" in wordList[0] and len(wordList) == 3:      # Create new Edge
                            self.addEdge(wordList[1], wordList[2])
                        elif "V" in wordList[0] and len(wordList) == 2:    # Create new Vertex
                            self.addVertex(wordList[0], wordList[1])
                        elif "L" in wordList[0] and len(wordList) == 5:    # Create new Launch
                            self.addLaunch(wordList[1],wordList[2],wordList[3],wordList[4])
            fh.close()
        except IOError:
            raise IOError
            
            
    def addEdge(self, va, vb):              
        "Adds new edge to edge list"
        existsVa = False
        existsVb = False 
        for e in self.edges:           
            if len(self.edges) == 1 and self.edges[0] == "E":# Checks if list is empty
                self.edges[0] = Edge()
                self.edges[0].newEdge(va, vb)           # If so, adds new edge
                existsVa = True
            else:
                if va == e.getMain():         # Checks if vertices in edge list.
                    existsVa = True             # If so, adds new connection.
                    if not e.isConnected(vb):   # If not, creates new edge (after for cycle)
                        e.add(vb)                   
                
                if vb == e.getMain():           # Same as if cycle above but 
                    existsVb = True             # with main vertex vb
                    if not e.isConnected(va):       
                        e.add(va)                   

        if not existsVa:                    # Adds new Edge to edge list w/main vertex va
            a = Edge()
            self.edges.append(a.newEdge(va, vb))
            
        if not existsVb:                    # Adds new Edge to edge list w/main vertex vb
            b = Edge()
            self.edges.append(b.newEdge(vb, va))
            
    def addVertex(self, name, weight):      
        "Adds new vertex to vertex list"
        exists = False
        for v in self.vertices:
            if len(self.vertices) == 1 and self.vertices[0] == "V":# Checks if list is empty       
                self.vertices[0] = Vertex()                     # If so, adds new vertex
                self.vertices[0].newVertex(name, weight)   
                exists = True
            elif name == v.getName():       # If vertex in vertex list, do nothing
                exists = True
            
        if not exists:                      # If not in list, add vertex
            V = Vertex()                  
            self.vertices.append(V.newVertex(name, weight))
    
    def addLaunch(self, t, p, f, u):        
        "Adds new launch to launch list"
        exists = False
        for l in self.launches:
            if len(self.launches) == 1 and self.launches[0] == "L":   # Checks if list is empty
                self.launches[0] = Launch()
                self.launches[0].newLaunch(t, p, f, u)     # If so, adds new launch
                exists = True
            elif t == l.getDate():          # If launch in launch list, do nothing
                exists = True
                
        if not exists:                      # If not in list, add launch
            L = Launch()
            self.launches.append(L.newLaunch(t, p, f, u))
             
    def printGraph(self):                       
        "Prints graph content to console"
        
        print("Edges: \n")
        for e in self.getEdges():
            print(e.getMain(), e.getConn(), "\n")
        print("\nVertices: \n")
        for v in self.getVertices():
            print(v.getName(), v.getWeight(), "\n")
        print("\nLaunches: \n")
        for l in self.getLaunches():
            print(l.getDate(), l.getPayload(), l.getFixedCost(), l.getUnitCost(), "\n")
            
    def getConnections(self, Node): 
        "Returns all the connections of a node"
        for e in self.getEdges():
            if e.getMain() == Node:
                c = e.getConn()
        return c
    
    def getWeight(self, Node):
        "Gets weight of node 'Node'"
        for v in self.getVertices():
            if v.getName() == Node:
                return v.getWeight()
            
    def getTotalWeight(self, chain):
        "Gets total weight of a chain of nodes"
        weight = 0
        for n in chain:
            weight = weight + self.getWeight(n)
        return weight
    
    def getVertices(self):
        return self.vertices
    
    def getLaunches(self):
        return self.launches

    def getEdges(self):
        return self.edges
            