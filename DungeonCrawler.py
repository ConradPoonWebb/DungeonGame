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
   Creators of the random, math, and time modules for python. Thanks a ton."""

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
        if (posX < 0) or (posY < 0):
            return True
        elif posX not in list(range(self.fX)):
            return False
        elif posY not in list(range(self.fY)):
            return False
        elif (self.data[posY][posX] != ' '):
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
    
    def distFromPoint(self,posX1,posX2,posY1,posY2):
        """Find distance between two points"""
        xDiff = abs(posX2 - posX1)
        yDiff = abs(posY2 - posY1)
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
            if self.checkEmpty(currentX,currentY+1): #Check Down
                moveList.append((currentX,currentY+1))
            if self.checkEmpty(currentX,currentY-1): #Check Up
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
        """Create rooms based on a list of 
           coordinates (tuples)"""
        for coord in coords:
            self.createRoom(coord[0],coord[1],'?')
    
    def neighborRooms(self,posX,posY):
        """Check how many rooms are
           next to a space on the map"""
        count = 0
        if (self.checkEmpty(posX+1,posY) == False): #Check Right
            count += 1
        if (self.checkEmpty(posX-1,posY) == False): #Check Left
            count += 1
        if (self.checkEmpty(posX,posY+1) == False): #Check Down
            count += 1
        if (self.checkEmpty(posX,posY-1) == False): #Check Up
            count += 1
        return count
    
    def neighborRoomsPos(self,posX,posY):
        """Check where the neighboring
           rooms occupy"""
        direction = ['R','L','D','U']
        if (self.checkEmpty(posX+1,posY) == False): #Check Right
            direction.remove('R')
        if (self.checkEmpty(posX-1,posY) == False): #Check Left
            direction.remove('L')
        if (self.checkEmpty(posX,posY+1) == False): #Check Down
            direction.remove('D')
        if (self.checkEmpty(posX,posY-1) == False): #Check Up
            direction.remove('U')
        return direction

    def checkBranch(self,posX,posY):
        """Check the availability of
           a branch"""
        coords = []
        if self.neighborRooms(posX,posY) <= 2 and (self.checkEmpty(posX,posY) == False):
            posPlaces = []
            if self.checkEmpty(posX+1,posY): #Check Right
                posPlaces.append((posX+1,posY))
            if self.checkEmpty(posX-1,posY): #Check Left
                posPlaces.append((posX-1,posY))
            if self.checkEmpty(posX,posY+1): #Check Down
                posPlaces.append((posX,posY+1))
            if self.checkEmpty(posX,posY-1): #Check Up
                posPlaces.append((posX,posY-1))
            for coord in posPlaces:
                if coord[0] < 0 or coord [1] < 0:
                    continue
                if (self.neighborRooms(coord[0],coord[1]) <= 1) and (self.checkEmpty(coord[0],coord[1]) == True):
                    coords.append(coord)
        else:
            return False
        if len(coords) > 0:
            return True
        else:
            return False
    
    def branchCoords(self,posX,posY):
        """Find the coords of a branching
           coordinate"""
        posPlaces = []
        coords = []
        if self.checkEmpty(posX+1,posY): #Check Right
            posPlaces.append((posX+1,posY))
        if self.checkEmpty(posX-1,posY): #Check Left
            posPlaces.append((posX-1,posY))
        if self.checkEmpty(posX,posY+1): #Check Down
            posPlaces.append((posX,posY+1))
        if self.checkEmpty(posX,posY-1): #Check Up
            posPlaces.append((posX,posY-1))
        for coord in posPlaces:
            if coord[0] < 0 or coord [1] < 0:
                continue
            if (self.neighborRooms(coord[0],coord[1]) <= 1) and (self.checkEmpty(coord[0],coord[1]) == True):
                coords.append(coord)
        
        return coords
    
    def makeBranchEnd(self,posX,posY):
        """Branches should be roughly 2-5 units away
           from the starting coord"""
        maxDist = random.choice(list(range(2,6)))
        posPoints = []
        for row in range(0,self.fY): #Finding points
            for col in range(0,self.fX):
                if (row == posY) and (col == posX):
                    continue
                if self.distFromPoint(posX,col,posY,row) <= maxDist:
                    if not(self.distFromPoint(posX,col,posY,row) < 2):
                        posPoints.append((col,row))
        
        posDirect = self.neighborRoomsPos(posX,posY)

        for coord in posPoints: #Filter points
            if 'R' not in posDirect:
                if coord[0] > posX:
                    posPoints.remove(coord)
                    continue
            if 'L' not in posDirect:
                if coord[0] < posX:
                    posPoints.remove(coord)
                    continue
            if 'D' not in posDirect:
                if coord[1] > posY:
                    posPoints.remove(coord)
                    continue
            if 'U' not in posDirect:
                if coord[1] < posY:
                    posPoints.remove(coord)
                    continue
            if self.neighborRooms(coord[0],coord[1]) > 1:
                posPoints.remove(coord)
                continue
            if self.checkEmpty(coord[0],coord[1]) == False:
                posPoints.remove(coord)
                continue
        
        c = random.choice(posPoints)
        while self.neighborRooms(c[0],c[1]) > 1:
            c = random.choice(posPoints)

        return c

    def pointToPoint(self,posX1,posY1,posX2,posY2):
        """Make a randomized path between 
           two points
           Add first point separately"""
        currentX,currentY = posX1,posY1
        path = []

        while self.distFromPoint(currentX,posX2,currentY,posY2) != 1.0:
            moveList = []
            moveDict = {}

            if self.checkEmpty(currentX+1,currentY): #Check Right
                moveList.append((currentX+1,currentY))
            if self.checkEmpty(currentX-1,currentY): #Check Left
                moveList.append((currentX-1,currentY))
            if self.checkEmpty(currentX,currentY+1): #Check Down
                moveList.append((currentX,currentY+1))
            if self.checkEmpty(currentX,currentY-1): #Check Up
                moveList.append((currentX,currentY-1))
            
            for coord in moveList:
                moveDict[coord] = self.distFromPoint(coord[0],posX2,coord[1],posY2)
            
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
        
        path.append((posX2,posY2))
        
        return path
    
    def checkPath(self,path):
        for coord in path:
            if self.neighborRooms(coord[0],coord[1]) >= 2:
                return False
        
        return True


#tests
d = Dungeon(5,5)
d.createEntrance(0,0)
d.createExit(0,4)
path = d.enterToExit()
d.createManyRooms(path)
#if d.checkBranch(1,0):
    #print(d.branchCoords(1,0))
    #print(d.makeBranchCoord(1,0))
if d.checkBranch(0,1):
    b = d.branchCoords(0,1)[0]
    print(b)
    bE = d.makeBranchEnd(0,1)
    while d.neighborRooms(bE[0],bE[1]) != 0: #REQUIRED IN FINAL CODE!!! This is the only way that works for some reason
        bE = d.makeBranchEnd(0,1)
    print(bE)
    d.createRoom(b[0],b[1],'?')
    p = d.pointToPoint(b[0],b[1],bE[0],bE[1])
    while d.checkPath(p) == False:
        p = d.pointToPoint(b[0],b[1],bE[0],bE[1])
    d.createManyRooms(p)
print(d)
