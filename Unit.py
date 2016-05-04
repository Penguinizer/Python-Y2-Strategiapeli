import Game
import Player
import random

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
        self.CurrentMovementPoints = MovementPoints
        self.Equipment = []
        self.UnitDeployed = False
        self.UnitColor = self.OwningPlayer.PlayerColor
        self.UnitCoordinates = None
        self.HasAttacked = False

    def ReduceHitPoints(self, num):
        self.HitPoints -= num
        return self.HitPoints

    def ReturnWeapon(self):
        for Equip in self.Equipment:
            if Equip.Type == "Weapon":
                return Equip
        return None

    def EquipItem(self, Equip):
        if Equip.Type=="Weapon":
            self.Equipment.append(Equip)
        elif Equip.Type== "Gear":
            self.Equipment.append(Equip)

            ## 1 on Hitpoints, 2 on Armor, 3 on Movement Points.
            if Equip.StatAffected == 1:
                self.HitPoints += Equip.Value

            elif  Equip.StatAffected == 2:
                self.Armor += Equip.Value

            elif  Equip.StatAffected == 3:
                self.MovementPoints += Equip.Value
                self.CurrentMovementPoints += Equip.Value


def CreateUnit(Player, UniqueID, UnitID):
    BaselineUnit = Player.Game.ReturnSpecificUnit(UnitID)
    ## Käytetään olemassa olevaa funktiota ja saadaan baseline unit jonka tiedot kopioidaan uuten, joka palautetaan.
    ## Player, UniqueID, UnitID, Name, Cost, UnitType, HitPoints, Armor, MovementPoints. Unit inputit.
    FinishedUnit = Unit(Player, UniqueID, UnitID, BaselineUnit.Name, BaselineUnit.Cost,
                        BaselineUnit.UnitType, BaselineUnit.HitPoints, BaselineUnit.Armor,
                        BaselineUnit.MovementPoints)

    return FinishedUnit

def AttackUnit(OwnTile, TargetTile):
        damage = OwnTile.UnitInSquare.ReturnWeapon().Damage
        armorpen = OwnTile.UnitInSquare.ReturnWeapon().ArmorPen
        optimalrange = OwnTile.UnitInSquare.ReturnWeapon().OptimalRange
        falloffrange = OwnTile.UnitInSquare.ReturnWeapon().FalloffRange
        accuracymodifier = TargetTile.AccuracyModifier

        distance = OwnTile.GetDistance(TargetTile)

        if distance <= optimalrange:
            unmoddamage = abs(round(damage*((0.7 * accuracymodifier + (random.random()*20))/100)))
            damagedealt = max(0, unmoddamage - max(0, (TargetTile.UnitInSquare.Armor - armorpen)))
            TargetTile.UnitInSquare.ReduceHitPoints(damagedealt)
            print("Damage dealt: " + str(damagedealt))
            print("Target HP Left: " + str(TargetTile.UnitInSquare.HitPoints))

            if TargetTile.UnitInSquare.HitPoints <= 0:
                TargetTile.UnitInSquare.OwningPlayer.PlayerUnitList.remove(TargetTile.UnitInSquare)
                TargetTile.UnitInSquare = None
                print("Target Dead")

        elif optimalrange < distance <= falloffrange:
            unmoddamage = abs(round(damage*((0.7 * accuracymodifier + (random.random()*20))/100)))
            damagedealt = max(0, unmoddamage - max(0, (TargetTile.UnitInSquare.Armor - armorpen)))
            TargetTile.UnitInSquare.ReduceHitPoints(damagedealt)
            print("Damage dealt: " + str(damagedealt))
            print("Target HP Left: " + str(TargetTile.UnitInSquare.HitPoints))

            if TargetTile.UnitInSquare.HitPoints <= 0:
                TargetTile.UnitInSquare.OwningPlayer.PlayerUnitList.remove(TargetTile.UnitInSquare)
                TargetTile.UnitInSquare = None
                print("Target Dead")

        else:
            print("Out of range. No damage dealt.")