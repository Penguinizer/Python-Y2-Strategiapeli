import FileReader

##Sisältää peli instanssin tiedot. Tarkemmat tiedot teknisessä suunnitelmassa.

class Game(object):
    def __init__(self):
        ##Tiedot täytetään myöhemmin.
        self.Players = []
        self.HumanPlayerCount = 0
        self.AIPlayerCount = 0
        self.Map = None
        self.Turncounter = 0
        self.BaselineUnitArray = []
        self.BaselineEquipmentArray = []

        self.PopulateUnitArray()
        self.PopulateEquipmentArray()

    def AddPlayer(self, Player):
        ##Lisätään uusi pelaaja, lisätään yksi pelaajien määrään.
        self.Players.append(Player)
        self.Playercount += 1

    def AddMap(self, Map):
        ##Asetetaan kartta. Luodaan MapGen vaiheessa.
        self.Map = Map

    def SetPoints(self, Points):
        self.Pointcount = Points

    def IterateTurncounter(self):
        self.Turncounter += 1
        return self.Turncounter

    def ReturnSpecificUnit(self, UnitID):
        ##Palautetaan yksikkö jolla on haluttu UnitID. None jos ei löydy. Voidaan tarkistaa
        for Unit in self.BaselineUnitArray:
            if Unit.UnitID == UnitID:
                return Unit

        raise ValueError("Faulty UnitID")

    def ReturnSpecificEquipment(self, EquipmentID):
        for Equipment in self.BaselineEquipmentArray:
            if Equipment.EquipmentID == EquipmentID:
                return Equipment

        raise ValueError("Faulty EquipmentID")

    def PopulateUnitArray(self):
        ##Kutsuu funktion joka luke teksti-tiedoston. Täytetään tiedoston nimi myöhemmin.
        Filename = "UnitStats.txt"
        self.BaselineUnitArray = FileReader.Filereader(Filename, "Units")

    def PopulateEquipmentArray(self):
        ##Kutsuu funktion joka lukee equipment tiedot teksti-tiedostosta. Lisätään tiedoston nimi myöhemmin.
        Filename = "EquipmentStats.txt"
        self.BaselineEquipmentArray = FileReader.Filereader(Filename, "Equipment")