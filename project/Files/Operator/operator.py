# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:49:35 2017

@authors: Luís Rei   nº 78486
          João Girão nº 78761
"""

from datetime import date, timedelta
import copy as c
    
class Action:
    
    def __init__(self, actionSet):
        self.date = date(1, 1, 1)
        self.set = actionSet
        
    def __add__(self, day):    
        "Adds days to a date"
        date = self.date + timedelta(1)
        return date
    
    def __repr__(self):
        return "<Action %s %s>" % (self.set, self.date)

    def setDate(self, Date):
        "Updates date"
        self.date = c.deepcopy(Date)
        
    def printResult(self):
        "Prints result"
        return self.getWrittenDate(), ' '.join(self.set)
    
    def getDate(self):
        return self.date

    def getWrittenDate(self):
        s = self.date.isoformat()          # Gets date in format YYYY-MM-DD
        date = s[8:] + s[5:7] + s[0:4]  # Puts date in format DDMMYYYY
        return date
    
    def getSet(self):
        return self.set