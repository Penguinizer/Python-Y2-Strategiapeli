class Tile(object):
    def __init__(self, TileType, TerrainType, x, y):
        self.TileType = TileType
        self.TerrainType = TerrainType
        self.Location = (x,y)
        self.UnitInSquare = None

        ##Määritellään tile tyypin perusteella. Prosentti modifier. Väri alussa määrittyy vain tile tyypistä.
        ##Tulevaisuudessa määrittyy myös terrain typestä. Tällä hetkellä yksinkertainen versio.
        if TileType == 0:
            self.AccuracyModifier = 0
            self.Color = 0x1f1f14
        elif TileType == 1:
            self.AccuracyModifier = 50
            self.Color = 0x004d00
        elif TileType == 2:
            self.AccuracyModifier = 75
            self.Color = 0x33cc33
        else:
            self.AccuracyModifier = 100
            self.Color = 0xffff4d
        '''
        Terrain tyypit:
        0 = Impassable
        1 = Heavy
        2 = Light
        3 = Open
        '''

    def MoveUnit(self, TargetTile):
        ##Tarkistetaan onko viereinen ruutu.
        '''
        print("Tööt")
        print(self.Location)
        print(self.UnitInSquare)
        '''
        if self.UnitInSquare:
            '''
            print(self.UnitInSquare)
            print("Distance to square:")
            print(self.GetDistance(TargetTile))
            print("Total Movement:")
            print(self.UnitInSquare.MovementPoints)
            print("Current Movement:")
            print(self.UnitInSquare.CurrentMovementPoints)
            '''
            if self.GetDistance(TargetTile) == 1 and TargetTile.TileType != 0 and self.UnitInSquare.CurrentMovementPoints > 0:
                if TargetTile.TileType == 1:
                    ##print(TargetTile.Location)
                    self.UnitInSquare.CurrentMovementPoints -= 2
                    self.UnitInSquare.UnitCoordinates = TargetTile.Location
                    ##print(self.UnitInSquare.UnitCoordinates)
                    TargetTile.UnitInSquare=self.UnitInSquare
                    self.UnitInSquare = None
                    '''
                    print("After")
                    print(self.UnitInSquare)
                    print("Distance to square:")
                    print(self.GetDistance(TargetTile))
                    print("Total Movement:")
                    print(self.UnitInSquare.MovementPoints)
                    print("Current Movement:")
                    print(self.UnitInSquare.CurrentMovementPoints)
                    self.UnitInSquare = None
                    '''
                    return True

                else:
                    ##print(TargetTile.Location)
                    self.UnitInSquare.CurrentMovementPoints -= 1
                    self.UnitInSquare.UnitCoordinates = TargetTile.Location
                    TargetTile.UnitInSquare=self.UnitInSquare
                    ##print(self.UnitInSquare.UnitCoordinates)
                    self.UnitInSquare = None
                    '''
                    print("After")
                    print(self.UnitInSquare)
                    print("Distance to square:")
                    print(self.GetDistance(TargetTile))
                    print("Total Movement:")
                    print(self.UnitInSquare.MovementPoints)
                    print("Current Movement:")
                    print(self.UnitInSquare.CurrentMovementPoints)
                    self.UnitInSquare = None
                    '''
                    return True

    def GetDistance(self, TargetTile):
        distancex = abs(self.Location[0] - TargetTile.Location[0])
        distancey = abs(self.Location[1] - TargetTile.Location[1])
        distance = max(distancex, distancey)
        return distance