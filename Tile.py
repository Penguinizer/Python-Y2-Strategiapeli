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

    def ReturnTileType(self):
        return self.TileType

    def ReturnTerrainType(self):
        return self.TerrainType

    def ReturnLocoation(self):
        return self.Location

    def ReturnColor(self):
        return self.Color

    def ReturnAccuracyModifier(self):
        return self.AccuracyModifier

    def ReturnUnitInSquare(self):
        return self.UnitInSquare

    def SetUnitInSquare(self, Unit):
        self.UnitInSquare = Unit