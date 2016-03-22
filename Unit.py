import Game
import Player

class Unit(object):
    def __init__(self, Player, UniqueID, UnitID, Name, Cost, UnitType, HitPoints, Armor, MovementPoints):
        self.OwningPlayer = Player
        self.UniqueID = UniqueID
        self.UnitID = UnitID
        self.Name = Name
        self.Cost = Cost
        self.UnitType = UnitType
        self.HitPoints = HitPoints
        self.Armor = Armor
        self.MovementPoints = MovementPoints
        self.Equipment = []

    def ReturnPlayer(self):
        return self.OwningPlayer

    def ReturnUniqueID(self):
        return self.UniqueID

    def ReturnName(self):
        return self.Name

    def ReturnCost(self):
        return self.Cost

    def ReturnUnitType(self):
        return self.UnitType

    def ReturnHitPoints(self):
        return self.HitPoints

    def ReduceHitPoints(self, num):
        self.HitPoints -= num
        return self.HitPoints

    def RaiseHitPoints(self, num):
        self.HitPoints += num
        return self.HitPoints

    def ReturnArmor(self):
        return self.Armor

    def ReturnMovementPoints(self):
        return self.MovementPoints

    def ReduceMovementPoints(self, num):
        self.MovementPoints -= num
        return self.MovementPoints

    def ReturnEquipment(self):
        return self.Equipment

    def ReturnWeapon(self):
        for Equip in self.Equipment:
            if Equip.ReturnType() == 0:
                return Equip

    def EquipItem(self, Equip):
        if Equip.ReturnType()==0:
            self.Equipment.append(Equip)
        elif Equip.ReturnType()==1:
            self.Equipment.append(Equip)

            ## 1 on Hitpoints, 2 on Armor, 3 on Movement Points.
            if Equip.ReturnStatAffected() == 1:
                self.HitPoints += Equip.ReturnValue

            elif  Equip.ReturnStatAffected() == 2:
                self.Armor += Equip.ReturnValue

            elif  Equip.ReturnStatAffected() == 3:
                self.MovementPoints += Equip.ReturnValue



def CreateUnit(Player, UniqueID, UnitID):
    BaselineUnit = Player.GetGame().ReturnSpecificUnit(UnitID)
    ## Käytetään olemassa olevaa funktiota ja saadaan baseline unit jonka tiedot kopioidaan uuten, joka palautetaan.
    ## Player, UniqueID, UnitID, Name, Cost, UnitType, HitPoints, Armor, MovementPoints. Unit inputit.
    FinishedUnit = Unit(Player, UniqueID, UnitID, BaselineUnit.ReturnName, BaselineUnit.ReturnCost,
                        BaselineUnit.ReturnUnitType, BaselineUnit.ReturnHitPoints, BaselineUnit.ReturnArmor,
                        BaselineUnit.ReturnMovementPoints)

    return FinishedUnit