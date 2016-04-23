
class Player(object):
    def __init__(self, PlayerName, isAI, Game):
        self.Name = PlayerName
        self.isAI = isAI
        self.PlayerUnitList = []
        self.Game = Game
        self.PointsAvailable = 0
        self.PlayerColor = (0xFF,0xFF,0xFF)

    def ReturnSpecificUnit(self, UnitID):
        for Unit in self.PlayerUnitList:
            if Unit.UnitID == UnitID:
                return Unit

        else:
            return None
            ##Tarkistetaan kutsuvassa funktiossa jotta voidaan käsitellä sillä puolella.