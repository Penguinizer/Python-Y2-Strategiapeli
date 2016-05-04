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

    winningplayer = None
    gamewon = False

    attackmode = False

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
            ##AI deployaa 4 ruutua vasemmasta reunasta, tekoäly 4 oikeasta.
            if unit.OwningPlayer.isAI == False:
                if clickedsquare[0]!= None and clickedsquare[1]!= None and Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare == None \
                        and not Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].TileType == 0 and clickedsquare[0]<=3:
                    Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare = unit
                    unit.UnitDeployed = True
                    unit.UnitCoordinates = (clickedsquare[0], clickedsquare[1])
            else:
                if clickedsquare[0]!= None and clickedsquare[1]!= None and Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare == None \
                        and not Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].TileType == 0 and clickedsquare[0]>=(xmax-4):
                    Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]].UnitInSquare = unit
                    unit.UnitDeployed = True
                    unit.UnitCoordinates = (clickedsquare[0], clickedsquare[1])
        return ReallyDeployUnitInSpace

    def EndPlayerTurn():
        nonlocal activeplayervar
        nonlocal activeplayer
        nonlocal  unitselected
        activeplayervar += 1

        if not unitselected in activeplayer.PlayerUnitList:
            unitselected = None

        for player in Game.Players:
            if len(player.PlayerUnitList) == 0:
                ##Poistaa pelaajat joiden kaikki yksiköt ovat tuhoutuneet pelistä.
                ## Eli tässä tapauksessa käytännössä hävinneen pelaajan.
                Game.Players.remove(player)
            if len(Game.Players) == 1:
                nonlocal gamewon
                nonlocal winningplayer
                gamewon = True
                winningplayer = Game.Players[0]

        for player in Game.Players:
            for unit in player.PlayerUnitList:
                unit.CurrentMovementPoints = unit.MovementPoints
                unit.HasAttacked = False
                if unit.UnitCoordinates == None:
                    player.PlayerUnitList.remove(unit)

        if activeplayervar < len(Game.Players):
            activeplayer = Game.Players[activeplayervar]
        elif not gamewon:
            Game.Turncounter += 1
            activeplayer = Game.Players[0]
            activeplayervar = 0

    def MoveUnit():
        if unitselected:
            if unitselected.OwningPlayer == activeplayer:
                ##print(unitselected.UnitCoordinates)
                Game.Map.MapMatrix[unitselected.UnitCoordinates[0]][unitselected.UnitCoordinates[1]].\
                    MoveUnit(Game.Map.MapMatrix[clickedsquare[0]][clickedsquare[1]])
                ##print(unitselected.UnitCoordinates)

    def ToggleAttackMode():
        nonlocal attackmode
        attackmode = not attackmode

    def AttackWithUnit(targettile):
        def ReallyAttackWithUnit():
            nonlocal unitselected
            if unitselected and (unitselected in activeplayer.PlayerUnitList):
                if unitselected != targettile.UnitInSquare and unitselected.OwningPlayer == activeplayer and not unitselected.HasAttacked:
                    ##AttackUnit(OwnTile, TargetTile):
                    ##print(targettile)
                    ##print(targettile.UnitInSquare)
                    Unit.AttackUnit(Game.Map.MapMatrix[unitselected.UnitCoordinates[0]][unitselected.UnitCoordinates[1]], targettile)
                    unitselected.HasAttacked = True
        return ReallyAttackWithUnit

    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        ##Tekoäly roina tän alle.
        if activeplayer.isAI and not gamewon:
            for aiunit in activeplayer.PlayerUnitList:
                print("Acting Unit: " + aiunit.Name + ", " +str(aiunit.UniqueID))
                ##Painotetaan eri ruutuja jotta päätetään mihin liikutaan.
                donemoving = False
                getstuckiter = 0
                while aiunit.CurrentMovementPoints > 0 and not donemoving:
                    csvar= 0
                    nvar = 0
                    svar= 0
                    wvar= 0
                    evar = 0
                    ## Välttää sitä että movement looppi jumittuu. Jos looppia suoritetaan viidettä kertaa, iskee tämä sen poikki.
                    getstuckiter += 1
                    if getstuckiter >= 5:
                        donemoving=True

                    for player in Game.Players:
                        if not player.isAI:
                            for playerunit in player.PlayerUnitList:
                                ##Käydään käsiksi ruutuihin pitkää reittiä. Näyttää monimutkasemmalta kun on.
                                ##Jos vihollinen on optimaalisella etäisyydellä, halutaan varmaan pysyä hyvässä paikassa.
                                if Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].GetDistance(Game.Map.MapMatrix[playerunit.UnitCoordinates[0]][playerunit.UnitCoordinates[1]])\
                                        <= aiunit.ReturnWeapon().OptimalRange:
                                    csvar += 2

                                if aiunit.UnitCoordinates[0] < playerunit.UnitCoordinates[0]:
                                    evar += 1
                                elif aiunit.UnitCoordinates[0] > playerunit.UnitCoordinates[0]:
                                    wvar += 1

                                if aiunit.UnitCoordinates[1] < playerunit.UnitCoordinates[1]:
                                    nvar += 1
                                elif aiunit.UnitCoordinates[1] > playerunit.UnitCoordinates[1]:
                                    svar += 1

                    ##Tarkastetaan minkälaista terrainia ruudulla on. Lisätään se painostusarvoon.
                    csquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]]
                    if csquare:
                        if csquare.TileType != 0:
                            csvar += 3 - csquare.TileType

                    if aiunit.UnitCoordinates[0] > 0 and aiunit.UnitCoordinates[1] > 0:
                        nwsquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]-1][aiunit.UnitCoordinates[1]-1]
                        if nwsquare:
                            if nwsquare.TileType != 0:
                                nvar += 3 - nwsquare.TileType
                                wvar += 3 - nwsquare.TileType
                    if aiunit.UnitCoordinates[1] > 0:
                        nsquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]-1]
                        if nsquare:
                            if nsquare.TileType != 0:
                                nvar += 3 - nsquare.TileType

                    if aiunit.UnitCoordinates[0] > 0:
                        wsquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]-1][aiunit.UnitCoordinates[1]]
                        if wsquare:
                            if wsquare.TileType != 0:
                                wvar += 3 - wsquare.TileType

                    if aiunit.UnitCoordinates[0] < (xmax-1) and aiunit.UnitCoordinates[1] > 0:
                        nesquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]+1][aiunit.UnitCoordinates[1]-1]
                        if nesquare:
                            if nesquare.TileType != 0:
                                nvar += 3 - nesquare.TileType
                                evar += 3 - nesquare.TileType

                    if aiunit.UnitCoordinates[0] < (xmax-1):
                        esquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]+1][aiunit.UnitCoordinates[1]]
                        if esquare:
                            if esquare.TileType != 0:
                                evar += 3 - esquare.TileType

                    if aiunit.UnitCoordinates[0] < (xmax-1) and aiunit.UnitCoordinates[1] < (ymax-1):
                        sesquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]+1][aiunit.UnitCoordinates[1]+1]
                        if sesquare:
                            if sesquare.TileType != 0:
                                evar += 3 - sesquare.TileType
                                svar += 3 - sesquare.TileType

                    if aiunit.UnitCoordinates[0] > 0 and aiunit.UnitCoordinates[1] < (ymax-1):
                        swsquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]-1][aiunit.UnitCoordinates[1]+1]
                        if swsquare:
                            if swsquare.TileType != 0:
                                wvar += 3 - swsquare.TileType
                                svar += 3 - swsquare.TileType

                    if aiunit.UnitCoordinates[1] < (ymax-1):
                        ssquare = Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]+1]
                        if ssquare:
                            if ssquare.TileType != 0:
                                svar += 3 - ssquare.TileType
                    ##Käytetään tietoa ja liikutaan suuntaan jolla on isoin arvo.
                    print("Square variables: Current: " + str(csvar) + ", N: " + str(nvar) + ", E: " + str(evar) + ", S: "
                          + str(svar) + ", W: " + str(wvar))

                    squarevars = [("cs", csvar),("n", nvar),("e", evar),("s", svar), ("w", wvar)]
                    maxsquare = max(squarevars, key = lambda t: t[1])
                    print(maxsquare)
                    if maxsquare[0] == "cs":
                        print("Staying in place.")
                        donemoving = True

                    elif maxsquare[0] == "n":
                        print("Moving north.")
                        Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].MoveUnit(Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]-1])

                    elif maxsquare[0] == "e":
                        print("Moving east.")
                        Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].MoveUnit(Game.Map.MapMatrix[aiunit.UnitCoordinates[0]+1][aiunit.UnitCoordinates[1]])

                    elif maxsquare[0] == "s":
                        print("Moving south")
                        Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].MoveUnit(Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]+1])

                    elif maxsquare[0] == "w":
                        print("Moving west")
                        Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].MoveUnit(Game.Map.MapMatrix[aiunit.UnitCoordinates[0]-1][aiunit.UnitCoordinates[1]])

                    if aiunit.CurrentMovementPoints <= 1:
                        donemoving = True

                ##Hankitaan etäisyys kaikkiin pelaajan yksiköihin ja sitten hyökätään lähimpään.
                distancestoenemies = []
                for player in Game.Players:
                    if not player.isAI:
                        for playerunit in player.PlayerUnitList:
                            distancestoenemies.append((Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]].GetDistance(Game.Map.MapMatrix[playerunit.UnitCoordinates[0]][playerunit.UnitCoordinates[1]]),playerunit))
                if distancestoenemies:
                    print("Attacking closest enemy: " + min(distancestoenemies, key = lambda t: t[0])[1].Name)
                    Unit.AttackUnit(Game.Map.MapMatrix[aiunit.UnitCoordinates[0]][aiunit.UnitCoordinates[1]], Game.Map.MapMatrix[min(distancestoenemies, key = lambda t: t[0])[1].UnitCoordinates[0]][min(distancestoenemies, key = lambda t: t[0])[1].UnitCoordinates[1]])

            EndPlayerTurn()

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
            Button(pygame.Rect(size[0]-475, size[1]-100, 200, 100), "Selected Tile: X: "+str(clickedsquare[0])+", Y: "+str(clickedsquare[1]), White, White, screen, 14)
            Button(pygame.Rect(25, size[1]-175, 100, 150), "Next Player", Green, White, screen, 14, ConfirmDeployment)
            ##Piirtää ei-deployatut yksiköt ala-palkkiin.
            for unittodeploy in Game.Players[deployingplayeriterator].PlayerUnitList:
                if unitplacementiterator < deploymentunitspace and not unittodeploy.UnitDeployed:
                    Button(pygame.Rect((150+unitplacementiterator*100), (size[1]-200), 100, 100), unittodeploy.Name, Green, unittodeploy.UnitColor, screen, 14, DeployUnitInSpace(unittodeploy))
                    Button(pygame.Rect((150+unitplacementiterator*100), (size[1]-120), 100, 20), "HP: " + str(unittodeploy.HitPoints) + ", MP: " + str(unittodeploy.CurrentMovementPoints),
                                        Green, unittodeploy.UnitColor, screen, 12)
                elif not unittodeploy.UnitDeployed:
                    Button(pygame.Rect((-250+unitplacementiterator*100), (size[1]-100), 100, 100), unittodeploy.Name, Green, unittodeploy.UnitColor, screen, 14, DeployUnitInSpace(unittodeploy))
                    Button(pygame.Rect((-250+unitplacementiterator*100), (size[1]-20), 100, 20), "HP: " + str(unittodeploy.HitPoints) + ", MP: " + str(unittodeploy.CurrentMovementPoints),
                                        Green, unittodeploy.UnitColor, screen, 12)
                unitplacementiterator += 1

        #Unit statseja displayavaa boksi
        if unitselected and UnitsDeployed:
            unitstatsboxupper = pygame.Rect(size[0]-675, size[1]-200, 400, 50)
            unitstatsboxlower = pygame.Rect(size[0]-675, size[1]-150, 400, 50)
            Button(pygame.Rect(size[0]-775, size[1]-200, 100,200), "Deselect Unit", Green, White, screen, 12, DeselectUnit)
            Button(pygame.Rect(size[0]-775, size[1]-25, 100,25), str(clickedsquare[0])+','+str(clickedsquare[1]), White, White, screen, 12)
            ##Printtaa yksikön statit boksiin.
            if unitselected:
                TextCenterer.ButtonText("Name: " + unitselected.Name + ", Owner: " +unitselected.OwningPlayer.Name + ", HP: " +
                                        str(unitselected.HitPoints) + ", MP: " + str(unitselected.CurrentMovementPoints) + ", Arm: " +
                                        str(unitselected.Armor),unitstatsboxupper, Black, 13).draw(screen)
                TextCenterer.ButtonText("Attack Damage: " + str(unitselected.ReturnWeapon().Damage) + ", Optimal Range: " + str(unitselected.ReturnWeapon().OptimalRange)
                                        + ", Falloff: " +str(unitselected.ReturnWeapon().FalloffRange)+ ", AP: " + str(unitselected.ReturnWeapon().ArmorPen)+ ", Can Attack: "
                                        + str(not unitselected.HasAttacked) ,unitstatsboxlower, Black, 13).draw(screen)

        ##Aktiivisen pelaajan vuoroindikaattori:
        if UnitsDeployed:
            Button(pygame.Rect(size[0]-475, size[1]-100, 200, 50),"Active Player: "+activeplayer.Name, White, White, screen, 14)
            Button(pygame.Rect(size[0]-475, size[1]-50, 200, 50), "", activeplayer.PlayerColor, activeplayer.PlayerColor, screen, 1)

        ##Turn end nappi
        if UnitsDeployed:
            Button(pygame.Rect(size[0]-675, size[1]-100, 200, 100),"End Turn", Green, White, screen, 14, EndPlayerTurn)

        ##Itse Kartta.
        ##Identtinen versio hyökkäämiselle. Sisältää eri funktion sen mahdollistamiseksi.
        ##Renderoituu samalla tavalla.
        if attackmode:
            for y in range(0, ysquarestorender):
                for x in range(0, xsquarestorender):
                    Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x), (size[1]/2)-(yspace*50)-100+(100*y), 100, 100),
                        str(x+xmapscrollvar)+','+str(y+ymapscrollvar), Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color,
                        Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color, screen, 25,
                        ReturnClickedSquare(x+xmapscrollvar, y+ymapscrollvar))
                    ##Valitun yksikön renderointi kullanvärisenä.
                    if Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare and Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare == unitselected:
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+10, 80, 80),
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.Name, Green,
                            (218,165,32), screen, 12, AttackWithUnit(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar]))
                        if Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare:
                            Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+70, 80, 20),
                                "HP: "+ str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.HitPoints) +
                                ", MP: " + str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.CurrentMovementPoints),
                                Green, (218,165,32), screen, 12)
                    ##Yksikön normaali renderointi.
                    elif Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare:
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+10, 80, 80),
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.Name, Green,
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.UnitColor
                            , screen, 12, AttackWithUnit(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar]))
                        if Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare:
                            Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+70, 80, 20),
                                "HP: "+ str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.HitPoints) +
                                ", MP: " + str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.CurrentMovementPoints),
                                Green,  Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.UnitColor, screen, 12)
        ##normaali kartanpiirto.
        else:
            for y in range(0, ysquarestorender):
                for x in range(0, xsquarestorender):
                    ##Piirtä kartta ruudun, funktio tekee siitä valittavan.
                    Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x), (size[1]/2)-(yspace*50)-100+(100*y), 100, 100),
                        str(x+xmapscrollvar)+','+str(y+ymapscrollvar), Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color,
                        Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].Color, screen, 25,
                        ReturnClickedSquare(x+xmapscrollvar, y+ymapscrollvar))
                    ##Piirtää yksikön kultaiseksi jos se on valittu.
                    if Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare and Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare == unitselected:
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+10, 80, 80),
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.Name, Green,
                            (218,165,32), screen, 12, SelectUnit(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare))
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+70, 80, 20),
                               "HP: "+ str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.HitPoints) +
                               ", MP: " + str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.CurrentMovementPoints),
                               Green, (218,165,32), screen, 12)
                    ##Piirtää yksikön pelaajan väriseksi jos sitä ei ole.
                    elif Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare:
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+10, 80, 80),
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.Name, Green,
                            Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.UnitColor
                            , screen, 12, SelectUnit(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare))
                        Button(pygame.Rect((size[0]/2)-(xspace*50)+(100*x)+10, (size[1]/2)-(yspace*50)-100+(100*y)+70, 80, 20),
                               "HP: "+ str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.HitPoints) +
                               ", MP: " + str(Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.CurrentMovementPoints),
                               Green, Game.Map.MapMatrix[x+xmapscrollvar][y+ymapscrollvar].UnitInSquare.UnitColor, screen, 12)

        ##Attack/Move komentonapit
        if UnitsDeployed:
            if attackmode:
                Button(pygame.Rect(25, size[1]-175, 200, 75), "Attack Mode Off", Green, Green, screen, 14, ToggleAttackMode)
            else:
                Button(pygame.Rect(25, size[1]-175, 200, 75), "Attack Mode On", Green, White, screen, 14, ToggleAttackMode)

            Button(pygame.Rect(25, size[1]-100, 200, 75), "Move Selected Unit", Green, White, screen, 14, MoveUnit)

        ##Current Turn boksi:
        Button(pygame.Rect(size[0]-100, 0, 100, 30), "Turn:"+str(Game.Turncounter), White, White, screen, 14)

        ##Winning player boksi:
        if gamewon:
            Button(pygame.Rect((size[0]/2)-200, (size[1]/2)-150, 400, 300), "Winning Player:" + winningplayer.Name, White, White, screen, 25)
            Button(pygame.Rect((size[0]/2)-100, (size[1]/2)+25, 200, 100), "End Game", Green, White, screen, 20, QuitGame)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])