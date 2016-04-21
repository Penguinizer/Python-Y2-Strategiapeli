class Tile(object):
    def __init__(self,TileType, TerrainType, y, x):
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

    def SetUnitInSquare(self, Unit):
        self.UnitInSquare = Unit
        return True

    def MoveUnit(self, TargetTile):
        ##Tarkistetaan onko viereinen ruutu.
        if self.GetDistance(TargetTile) > 1:
            return False
        ## Tarkistetaan voiko ruutuun edes liikkua.
        elif TargetTile.TileType == 0:
            return False
        elif TargetTile.TileType == 1 and self.UnitInSquare.MovementPoints <= 1:
            return False
        elif self.UnitInSquare.MovementPoints == 0:
            return False

        if TargetTile.TileType == 1:
            self.UnitInSquare.MovementPoints -= 2
            TargetTile.SetUnitInSquare(self.UnitInSquare)
            self.UnitInSquare = None
            return True

        else:
            self.UnitInSquare.MovementPoints -= 1
            TargetTile.SetUnitInSquare(self.UnitInSquare)
            self.UnitInSquare = None
            return True

    def GetDistance(self, TargetTile):
        distancex = self.Location[0] - TargetTile.Location[0]
        distancey = self.Location[1] - TargetTile.Location[1]
        distance = max(distancex, distancey)
        return distance