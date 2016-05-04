import FileReader

##Sisältää peli instanssin tiedot. Tarkemmat tiedot teknisessä suunnitelmassa.

class Game(object):
    def __init__(self):
        ##Tiedot täytetään myöhemmin.
        self.Players = []
        self.HumanPlayerCount = 0
        self.AIPlayerCount = 0
        self.Map = None
        self.Turncounter = 1
        self.BaselineUnitArray = []
        self.BaselineEquipmentArray = []

        self.PopulateUnitArray()
        self.PopulateEquipmentArray()

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
        ##Kutsuu funktion joka lukee teksti-tiedoston.
        Filename = "UnitStats.txt"
        self.BaselineUnitArray = FileReader.Filereader(Filename, "Units")

    def PopulateEquipmentArray(self):
        ##Kutsuu funktion joka lukee equipment tiedot teksti-tiedostosta.
        Filename = "EquipmentStats.txt"
        self.BaselineEquipmentArray = FileReader.Filereader(Filename, "Equipment")