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