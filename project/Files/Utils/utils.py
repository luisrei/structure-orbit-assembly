# Filename: Classes.py
"""
Created on Mon Oct 16 21:26:01 2017

Definition of classes Vertex, Edge and Launch needed for the execution of this 
project.

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from datetime import date

class Vertex:
    "Contains the name of the vertex 'v' and its correspondent weight 'w'"
    
    def __init__(self):             # Vertex constructor
        self.v = "Vij"   # Name of the vertex
        self.w = 0.0     # Weight of the vertex
    
    def newVertex(self, v, w):  # Creates new Vertex object
        self.setName(v)
        self.setWeight(w)
        return self
    
    def getWeight(self):        # Gets vertex's weight
        return self.w
    
    def getName(self):          # Gets vertex's name
        return self.v
    
    def setName(self, name):    # Sets vertex's weight
        self.v = name
        
    def setWeight(self, value): # Sets vertex's name
        self.w = float(value)    

class Edge:
    """
    Contains the name of its main vertex 'mainVertex' and a list of the names 
    of other vertices to which it is connected 'connections'
    """
    
    def __init__(self):      
        self.mainVertex = "Vij"     # Main vertex
        self.connections = []       # List of connections to other vertices
    
    def newEdge(self, va, vb):      # Creates new Edge object
        self.startEdge(va)
        self.add(vb)
        return self
    
    def startEdge(self, vertex):    
        "Defines edge's main vertex"
        self.mainVertex = vertex
    
    def add(self, vertex):          
        "Adds vertex to the list of connected vertices"
        self.connections.append(vertex)
        
    def isConnected(self, vertex):  
        "Checks if there is an edge between two vertices"
        if vertex in self.connections:
            return True
        else:
            return False
        
    def getMain(self):              
        "Gets main vertex's name"
        return self.mainVertex
    
    def getConn(self):
        "Gets main vertex's connections"
        return self.connections
    
class Launch:
    """
    Contains the launch date 't', the maximum payload allowed 'p', a fixed cost
    if the launch is done 'f' and the cost per unit of weight applied to all the
    components it takes 'u'
    """
    
    def __init__(self):
        self.t = date(1, 1, 1)          # Launch date format (YYYY, MM, DD)
        self.p = 0.0                    # Maximum launch payload
        self.f = 0.0                    # Fixed launch cost
        self.u = 0.0                    # Cost per unit of weight
    
    def newLaunch(self, t, p, f, u):    
        "Creates new Launch object"
        self.setDate(t)
        self.setPayload(p)
        self.setFixedCost(f)
        self.setUnitCost(u)
        return self
    
    def setDate(self, date):            
        "Sets launch date"
        day = int(date[0:2])    
        month = int(date[2:4])
        year = int(date[4:])
        self.t = self.t.replace(year, month, day)# Replaces date with desired one
        
    def setPayload(self, value):       
        "Sets max payload value"
        self.p = float(value)
        
    def setFixedCost(self, value):      
        "Sets fixed cost value"
        self.f = float(value)
        
    def setUnitCost(self, value):       
        "Sets variable cost value"
        self.u = float(value)
        
    def getDate(self):
        "Returns launch date"
        return self.t

    def getPayload(self):               
        "Gets payload value"
        return self.p    
    
    def getFixedCost(self):             
        "Gets fixed cost value"
        return self.f
    
    def getUnitCost(self):              
        "Gets variable cost value"
        return self.u
    

