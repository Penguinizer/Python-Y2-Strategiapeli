
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

    def GetPlayerName(self):
        return self.Name

    def GetAIProfile(self):
        return self.AIProfile

    def GetGame(self):
        return self.Game

    def TellIfIsAI(self):
        return self.isAI

    def AppendUnit(self, Unit):
        self.PlayerUnitList.append(Unit)

    def ReturnAllUnits(self):
        return self.PlayerUnitList

    def ReturnSpecificUnit(self, UnitID):
        for Unit in self.PlayerUnitList:
            if Unit.ReturnID() == UnitID:
                return Unit

        else:
            return None
            ##Tarkistetaan kutsuvassa funktiossa jotta voidaan käsitellä sillä puolella.