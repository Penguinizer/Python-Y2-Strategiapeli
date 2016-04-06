import json
import Unit
import Equipment

def Filereader(Filename, mode):
    array = []

    ## Avataan tiedosto, luetaan, käytetään json:ia parsettamiseen.
    with open(Filename, 'r') as f:
        for line in f:
            jsonline = json.loads(line)
            if (mode == "Units"):
                ##Player, UniqueID, UnitID, Name, Cost, UnitType, HitPoints, Armor, MovementPoints
                array.append(Unit.Unit("Baseline Unit", 0, jsonline.get("ID"), jsonline.get("Name"), jsonline.get("Cost"),
                                  jsonline.get("Unit Type"), jsonline.get("Hit Points"), jsonline.get("Armor"),
                                  jsonline.get("Movement Points")))
            elif (mode == "Equipment"):
               if jsonline.get("Type") == "Weapon":
                   ##Name, Cost, EquipmentID, Type, OptimalRange, FalloffRange, Damage, ArmorPen
                   array.append(Equipment.Weapon(jsonline.get("Name"), jsonline.get("Cost"), jsonline.get("ID"),
                                                 jsonline.get("Type"), jsonline.get("Optimal Range"), jsonline.get("Falloff Range"),
                                                 jsonline.get("Damage"), jsonline.get("Armor Penetration")))

               elif jsonline.get("Type") == "Gear":
                   ##Name, Cost, EquipmentID, Type, StatAffected, Value
                    array.append(Equipment.Gear(jsonline.get("Name"), jsonline.get("Cost"), jsonline.get("ID"),
                                                 jsonline.get("Type"), jsonline.get("Stat Affected"), jsonline.get("Value")))

    return array