class Equipment(object):
    def __init__(self, Name, Cost, EquipmentID, Type):
        self.Name = Name
        self.Cost = Cost
        self.EquipmentID = EquipmentID
        self.Type = Type

    def ReturnName(self):
        return self.Name

    def ReturnCost(self):
        return self.Cost

    def ReturnID(self):
        return self.EquipmentID

    def ReturnType(self):
        return self.Type

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

    def RetunOptimalRange(self):
        return self.OptimalRange

    def ReturnFalloffRange(self):
        return self.FalloffRange

    def ReturnDamage(self):
        return self.Damage

    def ReturnAP(self):
        return self.ArmorPen


class Gear(Equipment):
    def __init__(self, Name, Cost, EquipmentID, Type, StatAffected, Value):
        self.Name = Name
        self.Cost = Cost
        self.EquipmentID = EquipmentID
        self.Type = Type
        self.StatAffected = StatAffected
        self.Value = Value

    ## Stat Affected kertoo mihin geari vaikuttaa. 1 on Hitpoints, 2 on Armor, 3 on Movement Points.

    def ReturnStatAffected(self):
        return self.StatAffected

    def ReturnValue(self):
        return self.Value

def CreateEquipment(Player, EquipmentID):
    BaselineEquip = Player.GetGame().ReturnSpecificEquipment(EquipmentID)

    if BaselineEquip.ReturnType() == 0:
        ## Name, Cost, EquipmentID, Type, OptimalRange, FalloffRange, Damage, ArmorPen.
        ## Weapon Inputit
        NewEquip = Weapon(BaselineEquip.ReturnName(), BaselineEquip.ReturnCost(), BaselineEquip.ReturnID(),
                          BaselineEquip.ReturnType(), BaselineEquip.ReturnOptimalRange(), BaselineEquip.ReturnFalloffRange(),
                          BaselineEquip.ReturnDamage(), BaselineEquip.ReturnAP())

    elif BaselineEquip.ReturnType() == 1:
        NewEquip = Gear(BaselineEquip.ReturnName(), BaselineEquip.ReturnCost(), BaselineEquip.ReturnID(),
                        BaselineEquip.ReturnType(), BaselineEquip.ReturnStatAffected(), BaselineEquip.ReturnVale())

    return NewEquip