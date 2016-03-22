import FileReader

##Sisältää peli instanssin tiedot. Tarkemmat tiedot teknisessä suunnitelmassa.

class Game(object):
    def __init__(self):
        ##Tiedot täytetään myöhemmin.
        self.Players = []
        self.Playercount = 0
        self.Map = None
        self.Pointcount = 0
        self.Turncounter = 0
        self.BaselineUnitArray = []
        self.BaselineEquipmentArray = []

        self.PopulateUnitArray()
        self.PopulateEquipmentArray()

    def AddPlayer(self, Player):
        ##Lisätään uusi pelaaja, lisätään yksi pelaajien määrään.
        self.Players.append(Player)
        self.Playercount += 1

    def ReturnPlayers(self):
        return self.Players

    def ReturnPlayercount(self):
        return self.Playercount

    def AddMap(self, Map):
        ##Asetetaan kartta. Luodaan MapGen vaiheessa.
        self.Map = Map

    def ReturnMap(self):
        return self.Map

    def SetPoints(self, Points):
        self.Pointcount = Points

    def ReturnPointcount(self):
        return self.Pointcount

    def IterateTurncounter(self):
        self.Turncounter += 1

    def ReturnTurncounter(self):
        return self.Turncounter

    def ReturnUnits(self):
        return self.BaselineUnitArray

    def ReturnEquipment(self):
        return self.BaselineEquipmentArray

    def ReturnSpecificUnit(self, UnitID):
        ##Palautetaan yksikkö jolla on haluttu UnitID. None jos ei löydy. Voidaan tarkistaa
        for Unit in self.BaselineUnitArray:
            if Unit.ReturnEquipmentID() == UnitID:
                return Unit

        raise ValueError("Faulty UnitID")

    def ReturnSpecificEquipment(self, EquipmentID):
        for Equipment in self.BaselineEquipmentArray:
            if Equipment.ReturnEquipmentID() == EquipmentID:
                return Equipment

        raise ValueError("Faulty EquipmentID")

    def PopulateUnitArray(self):
        ##Kutsuu funktion joka luke teksti-tiedoston. Täytetään tiedoston nimi myöhemmin.
        Filename = "UnitStats.txt"
        self.BaselineUnitArray = FileReader.UnitReader(Filename)

    def PopulateEquipmentArray(self):
        ##Kutsuu funktion joka lukee equipment tiedot teksti-tiedostosta. Lisätään tiedoston nimi myöhemmin.
        Filename = "EquipmentStats.txt"
        self.BaselineEquipmentArray = FileReader.EquipmentReader(Filename)