import FileReader
import pygame
import math
import TextCenterer
from ButtonStuff import Button

import Unit
import Player

def GameplayLoop(InputGame):
    Game = InputGame
    clock = pygame.time.Clock()
    size = FileReader.Filereader("Config.txt", "ConfigSize")[0] ##Vaikka ton voi asettaa mielivaltasesti. Liian pieni arvo räjäyttää kaiken naamaan.
    screen = pygame.display.set_mode(size)
    gashunk = True
    Black = (0,0,0)
    White = (0xFF,0xFF,0xFF)
    Green = ((0,220,0))

    xspace = int(math.trunc(float(size[0])/100))
    yspace = int(math.trunc(float(size[1]-200)/100))
    xmax = Game.Map.MapSize[1]
    ymax = Game.Map.MapSize[0]
    xsquarestorender = min(xmax, xspace)
    ysquarestorender = min(ymax, yspace)
    xmapscrollvar = 0
    ymapscrollvar = 0

    clickedsquare = (None ,None)
    unitselected = None

    UnitsDeployed = False
    deployingplayeriterator = 0
    deploymentunitspace = int(math.trunc(float((size[0]-600))/100))

    activeplayervar = 0
    activeplayer = Game.Players[0]

    '''
    ##Testiroinaa:
    for player in Game.Players:
        for unit in player.PlayerUnitList:
            print(unit.Name)
            print(unit.Equipment)
    '''
    '''
    player = Player.Player("test", False, Game)
    unit = Unit.CreateUnit(player, 1, 1)
    unit.EquipItem(Game.BaselineEquipmentArray[1])
    Game.Map.MapMatrix[0][0].UnitInSquare = unit
    '''

    def QuitGame():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def MapScrollUp():
        nonlocal ymapscrollvar
        if ymapscrollvar < (ymax-yspace):
            ymapscrollvar += 1

    def MapScrollDown():
        nonlocal ymapscrollvar
        if ymapscrollvar > 0:
            ymapscrollvar -= 1

    def MapScrollLeft():
        nonlocal xmapscrollvar
        if xmapscrollvar > 0:
            xmapscrollvar -= 1

    def MapScrollRight():
        nonlocal xmapscrollvar
        if xmapscrollvar < (xmax-xspace):
            xmapscrollvar += 1

    def ReturnClickedSquare(x,y):
        def ReallyReturnClickedSquare():
            nonlocal clickedsquare
            clickedsquare = (x,y)
        return ReallyReturnClickedSquare

    def ConfirmDeployment():
        nonlocal deployingplayeriterator
        if deployingplayeriterator == len(Game.Players)-1:
            nonlocal UnitsDeployed
            UnitsDeployed = True
        else:
            deployingplayeriterator += 1

    def SelectUnit(unit):
        def ReallySelectUnit():
            nonlocal unitselected
            unitselected = unit
        return ReallySelectUnit

    def DeselectUnit():
        nonlocal unitselected
        unitselected = None

    def DeployUnitInSpace(unit):
        def ReallyDeployUnitInSpace():
            nonlocal clickedsquare
            ##Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare
            if clickedsquare[0]!= None and clickedsquare[1]!= None and Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare == None \
                    and not Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].TileType == 0:
                Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare = unit
                unit.UnitDeployed = True
        return ReallyDeployUnitInSpace

    def EndPlayerTurn():
        nonlocal activeplayervar
        nonlocal activeplayer
        activeplayervar += 1
        if activeplayervar < len(Game.Players):
            activeplayer = Game.Players[activeplayervar]
        else:
            Game.Turncounter += 1
            activeplayer = Game.Players[0]
            activeplayervar = 0

    def MoveUnit():
        print("Doot")

    def AttackUnit():
        print("Doot")

    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        ##Pelilogiikka roina tämän alle.


        ##Piirto koodi. Ensiksi ruutu valkoiseksi. Sitte scheissea ruutuun. Kaiken pitäis mennä fillin alapuolelle.
        screen.fill(White)
        ##Borderit ruudulle että näyttäis vähän paremmalta. Myös muita default roinia.
        ##Viiva rajaa alueen jossa on random control napit alueesta jossa on itse peli kartta.
        pygame.draw.rect(screen, Black, pygame.Rect(0,0,size[0],size[1]),3)
        pygame.draw.line(screen, Black, (0, size[1]-200), (size[0], size[1]-200), 3)
        if UnitsDeployed:
            pygame.draw.rect(screen, Black, (size[0]-675, size[1]-200, 400, 100), 3)
            pygame.draw.rect(screen, Black, (size[0]-775, size[1]-200, 100,200), 3)

        ##Map scroll napit.
        pygame.draw.line(screen, Black, (size[0]-275, size[1]), (size[0]-275, size[1]-200), 3)
        Nbutton = pygame.Rect(size[0]-175, size[1]-175, 75, 75)
        Wbutton = pygame.Rect(size[0]-250, size[1]-100, 75, 75)
        Sbutton = pygame.Rect(size[0]-175, size[1]-100, 75, 75)
        Ebutton = pygame.Rect(size[0]-100, size[1]-100, 75, 75)
        Button(Nbutton, "N", Green, White, screen, 25, MapScrollDown)
        Button(Wbutton, "W", Green, White, screen, 25, MapScrollLeft)
        Button(Sbutton, "S", Green, White, screen, 25, MapScrollUp)
        Button(Ebutton, "E", Green, White, screen, 25, MapScrollRight)

        ##Unittien deployaus
        if not UnitsDeployed:
            unitplacementiterator = 0
            Button(pygame.Rect(size[0]-475, size[1]-200, 200, 100), Game.Players[deployingplayeriterator].Name + " deploying", White, White, screen, 14)
            Button(pygame.Rect(size[0]-475, size[1]-100, 200, 100), "Selected Tile: X: "+str(clickedsquare[1])+", Y: "+str(clickedsquare[0]), White, White, screen, 14)
            Button(pygame.Rect(25, size[1]-175, 100, 150), "Next Player", Green, White, screen, 14, ConfirmDeployment)
            for unittodeploy in Game.Players[deployingplayeriterator].PlayerUnitList:
                if unitplacementiterator < deploymentunitspace and not unittodeploy.UnitDeployed:
                    Button(pygame.Rect((150+unitplacementiterator*100), (size[1]-200), 100, 100), unittodeploy.Name, Green, unittodeploy.UnitColor, screen, 16, DeployUnitInSpace(unittodeploy))
                elif not unittodeploy.UnitDeployed:
                    Button(pygame.Rect((-250+unitplacementiterator*100), (size[1]-100), 100, 100), unittodeploy.Name, Green, unittodeploy.UnitColor, screen, 16, DeployUnitInSpace(unittodeploy))
                unitplacementiterator += 1

        #Unit statseja displayavaa boksi
        if unitselected and UnitsDeployed:
            unitstatsboxupper = pygame.Rect(size[0]-675, size[1]-200, 400, 50)
            unitstatsboxlower = pygame.Rect(size[0]-675, size[1]-150, 400, 50)
            Button(pygame.Rect(size[0]-775, size[1]-200, 100,200), "Deselect Unit", Green, White, screen, 12, DeselectUnit)
            Button(pygame.Rect(size[0]-775, size[1]-25, 100,25), str(clickedsquare[0])+','+str(clickedsquare[1]), White, White, screen, 12)
            if unitselected:
                TextCenterer.ButtonText("Name: " + unitselected.Name + ", Owner: " +unitselected.OwningPlayer.Name + ", HP: " +
                                        str(unitselected.HitPoints) + ", MP: " + str(unitselected.MovementPoints) + ", Arm: " +
                                        str(unitselected.Armor),unitstatsboxupper, Black, 13).draw(screen)
                TextCenterer.ButtonText("Attack Damage: " + str(unitselected.ReturnWeapon().Damage) + ", Optimal Range: " + str(unitselected.ReturnWeapon().OptimalRange)
                                        + ", Falloff: " +str(unitselected.ReturnWeapon().FalloffRange)+ ", AP: " + str(unitselected.ReturnWeapon().ArmorPen),
                                        unitstatsboxlower, Black, 13).draw(screen)

        ##Aktiivisen pelaajan vuoroindikaattori:
        if UnitsDeployed:
            Button(pygame.Rect(size[0]-475, size[1]-100, 200, 50),"Active Player: "+activeplayer.Name, White, White, screen, 14)
            Button(pygame.Rect(size[0]-475, size[1]-50, 200, 50), "", activeplayer.PlayerColor, activeplayer.PlayerColor, screen, 1)

        ##Turn end nappi
        if UnitsDeployed:
            Button(pygame.Rect(size[0]-675, size[1]-100, 200, 100),"End Turn", Green, White, screen, 14, EndPlayerTurn)

        ##Attack/Move komentonapit
        if UnitsDeployed:
            Button(pygame.Rect(25, size[1]-175, 200, 75), "Attack With Unit", Green, White, screen, 14, AttackUnit)
            Button(pygame.Rect(25, size[1]-100, 200, 75), "Move Selected Unit", Green, White, screen, 14, MoveUnit)

        ##Itse Kartta. (size[0]/2)-(xspace*50)+(100*x), (size[1]/2)-(yspace*50)-200+(100*y), 100, 100
        for y in range(0, ysquarestorender):
            for x in range(0, xsquarestorender):
                Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x), (size[1]/2)-(yspace*50)-100+(100*y), 100, 100),
                       str(x+xmapscrollvar)+','+str(y+ymapscrollvar), Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color,
                       Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color, screen, 25,
                       ReturnClickedSquare(x+xmapscrollvar, y+ymapscrollvar))
                if Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare:
                    Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+10, 80, 80),
                           Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.Name, Green,
                           Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.UnitColor
                           , screen, 16, SelectUnit(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare))

        ##Current Turn boksi:
        Button(pygame.Rect(size[0]-100, 0, 100, 30), "Turn:"+str(Game.Turncounter), White, White, screen, 14)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])