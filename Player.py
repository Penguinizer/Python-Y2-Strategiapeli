
class Player(object):
    def __init__(self, PlayerName, AIConfig, Game):
        self.Name = PlayerName
        self.AIProfile = AIConfig
        self.isAI = None
        self.PlayerUnitList = []
        self.Game = Game

        if self.AIProfile != None:
            self.isAI = True
        else:
            self.isAI = False


    def ReturnSpecificUnit(self, UnitID):
        for Unit in self.PlayerUnitList:
            if Unit.UnitID == UnitID:
                return Unit

        else:
            return None
            ##Tarkistetaan kutsuvassa funktiossa jotta voidaan käsitellä sillä puolella.