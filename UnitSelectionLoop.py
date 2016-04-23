import pygame
from GameplayLoop import GameplayLoop
from ButtonStuff import Button
import FileReader
import Unit

def UnitSelection(InputGame):
    Game = InputGame
    clock = pygame.time.Clock()
    size = FileReader.Filereader("Config.txt", "ConfigSize")[0] ##Vaikka ton voi asettaa mielivaltasesti. Liian pieni arvo räjäyttää kaiken naamaan.
    screen = pygame.display.set_mode(size)
    gashunk = True
    Black = (0,0,0)
    White = (0xFF,0xFF,0xFF)
    Green = ((0,220,0))
    UnitsSelected = False
    unitlistlen = len(Game.BaselineUnitArray)
    equiplistlen = len(Game.BaselineEquipmentArray)
    unitscrollroom = max(0, (unitlistlen - 3))
    equipscrollroom = max(0, (equiplistlen -3))
    menuscrollvariable = 0
    pickingplayer = Game.Players[0]
    playeriterator = 0
    uniqueIDiterator = 0
    PickingGear = False
    newunit = None

    def QuitGame():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def ConfirmUnitsSelected():
        nonlocal pickingplayer
        nonlocal playeriterator
        playeriterator += 1
        if playeriterator == len(Game.Players):
            nonlocal UnitsSelected
            UnitsSelected = True
            GameplayLoop(Game)
        else:
            pickingplayer = Game.Players[playeriterator]

    def MenuDown():
        nonlocal menuscrollvariable
        nonlocal unitscrollroom
        nonlocal equipscrollroom
        if PickingGear == True:
            if menuscrollvariable < equipscrollroom:
                menuscrollvariable +=1
        else:
            if menuscrollvariable < unitscrollroom:
                menuscrollvariable += 1

    def MenuUp():
        nonlocal menuscrollvariable
        if menuscrollvariable > 0:
            menuscrollvariable -= 1

    def AddUnitSelectEquip(unit, player):
        def ReallyAddUnitSelectEquip():
            if player.PointsAvailable >= unit.Cost:
                nonlocal uniqueIDiterator
                nonlocal newunit
                nonlocal PickingGear
                nonlocal menuscrollvariable
                menuscrollvariable = 0
                uniqueIDiterator += 1
                newunit = Unit.CreateUnit(player, uniqueIDiterator, unit.UnitID)
                player.PointsAvailable -= newunit.Cost
                PickingGear = True
        return ReallyAddUnitSelectEquip

    def AddEquipToUnit(unit, equip, player):
        def ReallAddEquipToUnit():
            if equip.Type == "Weapon":
                if unit.ReturnWeapon() == None:
                    if player.PointsAvailable >= equip.Cost:
                        player.PointsAvailable -= equip.Cost
                        unit.EquipItem(equip)
            else:
                if player.PointsAvailable >= equip.Cost:
                    player.PointsAvailable -= equip.Cost
                    unit.EquipItem(equip)
        return ReallAddEquipToUnit

    def ConfirmEquip(newunit, player):
        def ReallyConfirmEquip():
            nonlocal newunit
            if newunit.ReturnWeapon() != None:
                nonlocal PickingGear
                nonlocal menuscrollvariable
                menuscrollvariable = 0
                player.PlayerUnitList.append(newunit)
                newunit = None
                PickingGear = False
        return ReallyConfirmEquip


    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        ##Olemassa sen takia, että muuten itse pelistä poistuminen iskisi takaisin tähän menuun.
        ##Saattaisi rikkoa asioita aika pahasti. Näin ollen, breakataan jotta palataan suoraan main menuun.
        if UnitsSelected == True:
            break

        ##Pelilogiikka roina
        menuxy = ((size[0]/2)-350, (size[1]/2)-250)

        ##Piirto koodi. Ensiksi ruutu valkoiseksi. Sitte scheissea ruutuun. Kaiken pitäis mennä fillin alapuolelle.
        screen.fill(White)
        ##Vakio roina kuten menu border ja sekalaiset viivat.
        menuborder = pygame.Rect(menuxy[0], menuxy[1], 700, 500)
        pygame.draw.rect(screen, Black, menuborder, 3)
        pygame.draw.line(screen, Black, (menuxy[0], menuxy[1]+375), (menuxy[0]+700, menuxy[1]+375), 3)

        ##Valitsevan pelaajan kertova juttu. Viereinen juttu kertoo jäljellä olevien pisteiden määrän.
        pickingplayerbox = pygame.Rect(menuxy[0], menuxy[1], 350, 75)
        playerpointsbox = pygame.Rect(menuxy[0]+350, menuxy[1], 350, 75)
        Button(pickingplayerbox, pickingplayer.Name, White, White, screen, 25)
        Button(playerpointsbox, "Points Available: " + str(pickingplayer.PointsAvailable), White, White, screen, 25)

        ##Listan scrollaus ylös ja alas
        upbutton = pygame.Rect(menuxy[0]+500, menuxy[1]+400, 75, 75)
        downbutton = pygame.Rect(menuxy[0]+600, menuxy[1]+400, 75, 75)
        Button(upbutton, "Up", Green, White, screen, 25, MenuUp)
        Button(downbutton, "Down", Green, White, screen, 25, MenuDown)

        ##Piirtää yksikkö boksit. 300 pikseliä tilaa. 3 yksikköboksia, 100 pikseliä korkeutta per.
        ##jos pikataan gearia niin tekee sen tässä.
        if PickingGear == True:
            gearstrings = []
            for gear in Game.BaselineEquipmentArray:
                if gear.Type == "Weapon":
                    gearstrings.append(gear.Name + ", Cost: " + str(gear.Cost) + ", Weapon, DMG: " + str(gear.Damage) + ", AP: "
                                       + str(gear.ArmorPen) + ", OR/FO: " + str(gear.OptimalRange)+ "/" + str(gear.FalloffRange))

                elif gear.Type == "Gear":
                    if gear.StatAffected == 1:
                        gearstrings.append(gear.Name +", Cost: " + str(gear.Cost) + ", Affects: HP, Amount: " + str(gear.Value))
                    elif gear.StatAffected == 2:
                        gearstrings.append(gear.Name +", Cost: " + str(gear.Cost) + ", Affects: Armor, Amount: " + str(gear.Value))
                    elif gear.StatAffected == 3:
                        gearstrings.append(gear.Name +", Cost: " + str(gear.Cost) + ", Affects: MP, Amount: " + str(gear.Value))

            for var in range(3):
                Button (pygame.Rect(menuxy[0], menuxy[1]+75+var*100, 700, 100), gearstrings[var + menuscrollvariable]
                       , Green, White, screen, 25, AddEquipToUnit(newunit, Game.BaselineEquipmentArray[var+menuscrollvariable], pickingplayer))
                ##AddEquipToUnit(newunit, Game.BaselineEquipmentArray[var+menuscrollvariable])

            Button(pygame.Rect(menuxy[0], menuxy[1]-75, 700, 75), "Confirm Unit Equipment", Green, White, screen, 25, ConfirmEquip(newunit, pickingplayer))

        elif PickingGear == False:
            unitstrings = []
            for unit in Game.BaselineUnitArray:
                unitstrings.append(unit.Name + ", Cost: " + str(unit.Cost) + ", Type: " + unit.UnitType + ", HP: "
                               + str(unit.HitPoints) + ", Armor: " + str(unit.Armor) + ", MP: " + str(unit.MovementPoints))
            for butts in range(3):
                Button(pygame.Rect(menuxy[0], menuxy[1]+75+butts*100, 700, 100), unitstrings[butts + menuscrollvariable]
                       ,Green, White, screen, 25, AddUnitSelectEquip(Game.BaselineUnitArray[butts+menuscrollvariable], pickingplayer))

        ##Confirm valinnat nappi
        if PickingGear == False:
            confirmbutton = pygame.Rect(menuxy[0]+25, menuxy[1]+400, 200, 75)
            Button(confirmbutton, "Confirm Selections", Green, White, screen, 25, ConfirmUnitsSelected)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])