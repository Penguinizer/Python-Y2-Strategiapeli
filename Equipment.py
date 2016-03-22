class Equipment(object):
    def __init__(self):


def CreateEquipment(Player, EquipmentID):
    BaselineEquip = Player.GetGame().ReturnSpecificEquipment(EquipmentID)
    