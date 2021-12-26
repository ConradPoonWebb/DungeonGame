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

import random
import time

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
           # - Boss room
           ? - Unknown room
        """
        self.data[posY][posX] = rType

#tests
d = Dungeon(10,10)
d.createEntrance(0,0)
d.createExit(9,9)
print(d)
