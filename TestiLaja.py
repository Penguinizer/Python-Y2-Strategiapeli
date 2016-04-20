import random
'''
Equipment subclass testi koodipätkä:

class Dongs(object):
    def __init__(self, Name):
        self.Name = Name

    def ReturnName(self):
        return self.Name

class Dickbutt(Dongs):
    def __init__(self, Name, Stuff):
        self.Name=Name
        self.Stuff=Stuff

    def ReturnStuff(self):
        return self.Stuff


Stuff = Dongs("Name")

print(Stuff.ReturnName())

OtherStuff = Dickbutt("Name", "Stuff")

print(OtherStuff.ReturnName())
print(OtherStuff.ReturnStuff())
'''

'''
Map luonti random.randint testipätkä koodia:

MapMatrix = [[y for x in range (0,5)] for y in range(0,4)]
print(MapMatrix)

print(MapMatrix[1][2])

random.seed()
print(random.randint(0,3))
print(random.randint(0,3))
print(random.randint(0,3))

XSize = 12
YSize = 12
MapMatrix = [[None for x in range (0,XSize)] for y in range(0,YSize)]
for y in range(0,XSize):
    for x in range(0,YSize):
        MapMatrix[y][x] = random.randint(0,10)

print(MapMatrix)

'''
'''
type = int(input("Select encounter type:\n 1: Gang\n 2: Corporate Securityn\n 3: KnightErrantTeam\n 4: Opposing Team\n "))
if 0 < type <= 4:
    print(type)

CorrectAnswer = False
try:
    MageMembers = abs(int(input("\n Select amount of mages: ")))
    CorrectAnswer = True
except ValueError:
    print("Requires Number.\n")

print(MageMembers)
print(CorrectAnswer)
'''
'''
import json
import Unit
array = []
mode = "Units"
Filename = "UnitStats.txt"
with open(Filename, 'r') as f:
        for line in f:
            jsonline = json.loads(line)
            if (mode == "Units"):
                ##Player, UniqueID, UnitID, Name, Cost, UnitType, HitPoints, Armor, MovementPoints
                array.append(Unit.Unit("Baseline Unit", 0, jsonline.get("ID"), jsonline.get("Name"), jsonline.get("Cost"),
                                  jsonline.get("Unit Type"), jsonline.get("Hit Points"), jsonline.get("Armor"),
                                  jsonline.get("Movement Points")))

print(array)
print(array[0].Name)
print(array[1].Name)

for unit in array:
    if unit.UnitID == 2:
        print(unit.Name)
'''
'''
import pygame
pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
'''
import pygame
import TextCenterer
import time

def Button(rect, text, ac, pc, screen, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, ac, rect)

        if click[0] == 1 and action != None:
            action()
            time.sleep(0.1)

    else:
        pygame.draw.rect(screen, pc, rect)

    pygame.draw.rect(screen, (0,0,0), rect, 3)

    text = TextCenterer.ButtonText(text, rect, (0,0,0))
    text.draw(screen)