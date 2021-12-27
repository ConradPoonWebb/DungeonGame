#Dungeon Crawler
#By Conrad Poon

"""Infinite randomized dungeon with loot
   and monsters
"""

"""TO DO/PLAN:
    class Dungeon - Creates a randomized dungeon
    class Enemies - Creates enemies with names/types and behavior?
    class Weapons - Creates weapons with description?
    class Players - Creates the main character and companions
    class Item - Creates an item in the dungeon. Maybe could include weapons?
    class Rooms - Creates details about
    class NPC(?) - Creates an NPC that can live/work in dungeon
       - Maybe add store system plus currency?
    Turn based battle system - Maybe with some graphics? Quite hard to do
    Descriptions of areas? - Could be cool I guess
"""

"""ACKNOWLEDGEMENTS:
   Base code courtesy of Harvey Mudd, from their Connect 4 homework project
   Creators of the random and time modules for python. Thanks a ton."""

"""Notes:
   Blue - 34
   Red - 31
   Green - 32
   
   ■ - Room with enemies
   □ - Room without enemies
   ✭ - Boss room
   ? - Unknown room"""

import random
import time
from math import sqrt

class Dungeon:
    """Creates a readable layout of a dungeon plus the
       dungeon itself. Also has types of rooms
    """
    def __init__(self, fX,fY):
        """Initiallizer. fX, fY, and the floor data"""
        self.fX = fX
        self.fY = fY
        self.data = [[' ']*fX for row in range(fY)]
    
    def __repr__(self):
        """Representation of floor
           Could be used in game?"""
        s = '' 
        for row in range(0, self.fY):
            s+= '|'
            for col in range(0, self.fX):
                s += self.data[row][col] + '|'
            s += '\n'
        return s
    
    def createEntrance(self,posX,posY):
        """Creates the entrance to the floor"""
        self.data[posY][posX] = '\033[1;32;40m'+'O'+'\033[0m'
    
    def createExit(self,posX,posY):
        """Creates the exit to the floor"""
        self.data[posY][posX] = '\033[1;31;40m'+'X'+'\033[0m'

    def createRoom(self,posX,posY,rType):
        """Creates a room to the floor
           rTypes:
           ■ - Room with enemies
           □ - Room without enemies
           ✭ - Boss room
           ? - Unknown room
        """
        self.data[posY][posX] = rType
    
    def checkEmpty(self,posX,posY):
        """Checks if a space is occupied
           by an element"""
        if posX not in range(self.fX):
            return False
        elif posY not in range(self.fY):
            return False
        elif (self.data[posY][posX] != ' ') or (self.data[posY][posX] == "\033[1;32;40mO\033[0m"):
            return False
        return True

    def findEnter(self):
        """Find the entrance
           For other function"""
        for row in range(self.fY):
            for col in range(self.fX):
                if self.data[row][col] == "\033[1;32;40mO\033[0m":
                    return col,row
    
    def findExit(self):
        """Find the exit
           For other function"""
        for row in range(self.fY):
            for col in range(self.fX):
                if self.data[row][col] == "\033[1;31;40mX\033[0m":
                    return col,row

    def distFromExit(self,posX,posY):
        """Find the distance from the exit"""
        exitX,exitY = self.findExit()

        xDiff = abs(exitX - posX)
        yDiff = abs(exitY - posY)
        dist = sqrt(xDiff + yDiff)

        return dist
    
    def enterToExit(self):
        """Create a path from the entrance
           to the exit
           For building rooms"""
        currentX,currentY = self.findEnter()
        path = []

        while self.distFromExit(currentX,currentY) != 1.0:
            moveList = []
            moveDict = {}

            if self.checkEmpty(currentX+1,currentY): #Check Right
                moveList.append((currentX+1,currentY))
            if self.checkEmpty(currentX-1,currentY): #Check Left
                moveList.append((currentX-1,currentY))
            if self.checkEmpty(currentX,currentY+1): #Check Up
                moveList.append((currentX,currentY+1))
            if self.checkEmpty(currentX,currentY-1): #Check Down
                moveList.append((currentX,currentY-1))
            
            for coord in moveList:
                moveDict[coord] = self.distFromExit(coord[0],coord[1])
            
            sort_moveDict = sorted(moveDict.items(), key=lambda x: x[1])
            
            if len(sort_moveDict) > 1:
                if (sort_moveDict[0][1] == sort_moveDict[1][1]) and (sort_moveDict[0][0] not in path):
                    closestCoord = sort_moveDict[random.choice([0,1])][0]
                elif sort_moveDict[0][0] in path:
                    closestCoord = sort_moveDict[1][0]
                else:
                    closestCoord = sort_moveDict[0][0]
            else:
                closestCoord = sort_moveDict[0][0]

            currentX,currentY = closestCoord[0],closestCoord[1]
            path.append((currentX,currentY))
        
        return path
    
    def createManyRooms(self,coords):
        for coord in coords:
            self.createRoom(coord[0],coord[1],'?')



#tests
d = Dungeon(5,5)
d.createEntrance(0,0)
d.createExit(2,3)
#d.createRoom(1,2,'■')
#d.createRoom(2,2,'□')
#d.createRoom(3,2,'✭')
#d.createRoom(4,2,'?')
path = d.enterToExit()
d.createManyRooms(path)
print(d)
