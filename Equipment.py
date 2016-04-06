class Equipment(object):
    def __init__(self, Name, Cost, EquipmentID, Type):
        self.Name = Name
        self.Cost = Cost
        self.EquipmentID = EquipmentID
        self.Type = Type

class Weapon(Equipment):
    def __init__(self, Name, Cost, EquipmentID, Type, OptimalRange, FalloffRange, Damage, ArmorPen):
        self.Name = Name
        self.Cost = Cost
        self.EquipmentID = EquipmentID
        self.Type = Type
        self.OptimalRange = OptimalRange
        self.FalloffRange = FalloffRange
        self.Damage = Damage
        self.ArmorPen = ArmorPen

class Gear(Equipment):
    def __init__(self, Name, Cost, EquipmentID, Type, StatAffected, Value):
        self.Name = Name
        self.Cost = Cost
        self.EquipmentID = EquipmentID
        self.Type = Type
        self.StatAffected = StatAffected
        self.Value = Value

    ## Stat Affected kertoo mihin geari vaikuttaa. 1 on Hitpoints, 2 on Armor, 3 on Movement Points.


def CreateEquipment(Player, EquipmentID):
    BaselineEquip = Player.Game.ReturnSpecificEquipment(EquipmentID)

    if BaselineEquip.ReturnType() == 0:
        ## Name, Cost, EquipmentID, Type, OptimalRange, FalloffRange, Damage, ArmorPen.
        ## Weapon Inputit
        NewEquip = Weapon(BaselineEquip.Name, BaselineEquip.Cost, BaselineEquip.EquipmentID,
                          BaselineEquip.Type, BaselineEquip.OptimalRange, BaselineEquip.FalloffRange,
                          BaselineEquip.Damage, BaselineEquip.ArmorPen)

    elif BaselineEquip.ReturnType() == 1:
        NewEquip = Gear(BaselineEquip.Name, BaselineEquip.Cost, BaselineEquip.EquipmentID,
                        BaselineEquip.Type, BaselineEquip.StatAffected, BaselineEquip.Value)

    return NewEquip