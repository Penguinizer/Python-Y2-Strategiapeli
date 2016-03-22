import random

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