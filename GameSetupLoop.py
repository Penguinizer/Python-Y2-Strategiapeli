import FileReader
import pygame
from UnitSelectionLoop import UnitSelection
from ButtonStuff import Button
from Game import Game
from Player import Player
from Map import Map

def GameSetup():
    clock = pygame.time.Clock()
    size = FileReader.Filereader("Config.txt", "ConfigSize")[0] ##Vaikka ton voi asettaa mielivaltasesti. Liian pieni arvo räjäyttää kaiken naamaan.
    screen = pygame.display.set_mode(size)
    gashunk = True
    Black = (0,0,0)
    White = (0xFF,0xFF,0xFF)
    Green = ((0,220,0))
    NewGame= Game()
    pointsamountsvar = 6
    PointsSet = False
    Playersadded = False
    MapAdded = False
    GameCreated = False
    Xvar = 20
    Yvar = 20
    TerrainType = None

    def QuitGame():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def StartGameCheck():
        ##Tarkistetaan onko kaikki asetettu oikein. Jos on siirytään itse peliin.
        if Playersadded and MapAdded:
            nonlocal GameCreated
            GameCreated = True
            UnitSelection(NewGame)

    def SetPoints(num, InputGame):
        def ReallySetPoints():
            for player in InputGame.Players:
                player.PointsAvailable = num
            nonlocal PointsSet
            PointsSet = True
        return ReallySetPoints

    def AddHumanPlayer():
        nonlocal NewGame
        NewGame.HumanPlayerCount += 1
        NewGame.Players.append(Player("Human Player #: " + str(NewGame.HumanPlayerCount), False, NewGame))

    def AddAIPlayer():
        nonlocal NewGame
        NewGame.AIPlayerCount += 1
        NewGame.Players.append(Player("AI Player #: " + str(NewGame.AIPlayerCount), True, NewGame))

    def ConfirmAddedPlayers():
        nonlocal NewGame
        if NewGame.HumanPlayerCount >= 1 and NewGame.AIPlayerCount >= 1:
            nonlocal Playersadded
            Playersadded = True

    def XIncrease():
        nonlocal Xvar
        Xvar += 1

    def XDecrease():
        nonlocal Xvar
        if Xvar > 10:
            Xvar -= 1

    def YIncrease():
        nonlocal Yvar
        Yvar += 1

    def YDecrease():
        nonlocal Yvar
        if Yvar > 10:
            Yvar -= 1

    def SetTerrain(var):
        def ActuallySetTerrain():
            nonlocal TerrainType
            TerrainType = var
        return ActuallySetTerrain()

    def ConfirmMap():
        if TerrainType and 10 < Xvar < 100  and 10 < Yvar < 100:
            nonlocal NewGame
            NewGame.Map = Map(Xvar, Yvar, TerrainType, NewGame)
            nonlocal MapAdded
            MapAdded = True

    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        ##Olemassa sen takia, että muuten itse pelistä poistuminen iskisi takaisin tähän menuun.
        ##Saattaisi rikkoa asioita aika pahasti. Näin ollen, breakataan jotta palataan suoraan main menuun.
        if GameCreated == True:
            break

        ##Rectejä roinaa varten.
        menuxy = ((size[0]/2)-350, (size[1]/2)-250)
        menuborders = pygame.Rect(menuxy[0], menuxy[1], 700, 500)
        completedstepsbox = pygame.Rect(menuxy[0],menuxy[1],700, 75)
        confirmbutton = pygame.Rect(menuxy[0]+25, menuxy[1]+400, 150, 75)
        quitbutton = pygame.Rect(menuxy[0]+200, menuxy[1]+400, 150, 75)

        ##Logiikka roinaa varten.
        ##Ensiksi lisätään pelaajia.
        if not Playersadded:
            humanplayer = pygame.Rect(menuxy[0]+50, menuxy[1]+100, 200, 100)
            aiplayer = pygame.Rect(menuxy[0]+300, menuxy[1]+100, 200, 100)
            confirmplayersbutton = pygame.Rect(menuxy[0]+50, menuxy[1]+250, 200, 100)

        ##Sitten valitaan pistemäärä. 100,200 jne. Tehdään loopilla koska copypasta on huonoa.
        elif not PointsSet and Playersadded:
            pointsrects = []
            for k in range(pointsamountsvar):
                if k <= 2:
                    pointsrects.append(pygame.Rect(((size[0]/2)-325)+k*175, menuxy[1]+100, 150, 75))
                else:
                    pointsrects.append(pygame.Rect(((size[0]/2)-325)+(k-3)*175, menuxy[1]+200, 150, 75))

        ##Napit kartan setuppia varten.
        elif not MapAdded and PointsSet and Playersadded:
            xincrease = pygame.Rect(menuxy[0]+25, menuxy[1]+100, 75, 75)
            xcurrent = pygame.Rect(menuxy[0]+100,menuxy[1]+100, 100, 75)
            xdecrease = pygame.Rect(menuxy[0]+200, menuxy[1]+100, 75, 75)
            yincrease = pygame.Rect(menuxy[0]+25, menuxy[1]+200, 75, 75)
            ycurrent = pygame.Rect(menuxy[0]+100, menuxy[1]+200, 100, 75)
            ydecrease = pygame.Rect(menuxy[0]+200, menuxy[1]+200, 75, 75)
            terraintypefirst = pygame.Rect(menuxy[0]+300, menuxy[1]+100, 200, 75)
            terraintypesecond = pygame.Rect(menuxy[0]+300, menuxy[1]+200, 200, 75)
            confirmmap = pygame.Rect(menuxy[0]+300, menuxy[1]+300, 200, 75)

        ##Piirto koodi. Ensiksi ruutu valkoiseksi. Sitte scheissea ruutuun. Kaiken pitäis mennä fillin alapuolelle.
        screen.fill(White)
        ##Napit jotka aina paikoillaan.
        pygame.draw.rect(screen, Black, menuborders, 3)
        Button(confirmbutton, "Start Game", Green, White, screen, StartGameCheck)
        Button(quitbutton, "Main Menu", Green, White, screen, QuitGame)
        ##Näytetään missä vaiheessa game setuppia ollaan.
        Button(completedstepsbox, "Steps Completed: Players: " + str(Playersadded) +", Points: " + str(PointsSet) +", Map: " + str(MapAdded), White, White, screen)
        ##Napit Pelaajien lisäämistä varten
        if not Playersadded:
            Button(humanplayer, "Add Human Player", Green, White, screen, AddHumanPlayer)
            Button(aiplayer, "Add AI Player", Green, White, screen, AddAIPlayer)
            Button(confirmplayersbutton, "Confirm Players", Green, White, screen, ConfirmAddedPlayers)
        ##Napit pisteiden asettamista varten.
        elif not PointsSet and Playersadded:
            for k in range(pointsamountsvar):
                Button(pointsrects[k], str(300+k*100) + "Points", Green, White, screen, SetPoints((100+k*100), NewGame))
        ##Napit kartan lisäämistä varten.
        elif not MapAdded and PointsSet and Playersadded:
            Button(xincrease, "+ X", Green, White, screen, XIncrease)
            Button(xdecrease, "- X", Green, White, screen, XDecrease)
            Button(xcurrent, "X: "+str(Xvar), White, White, screen)
            Button(yincrease, "+ Y", Green, White, screen, YIncrease)
            Button(ydecrease, "- Y", Green, White, screen, YDecrease)
            Button(ycurrent, "Y: "+str(Yvar),White, White, screen)
            Button(terraintypefirst, "Terrain Type: Hot", Green, White, screen, SetTerrain("Hot"))
            Button(terraintypesecond, "Terrain Type: Cold", Green, White, screen, SetTerrain("Cold"))
            Button(confirmmap, "Confirm Map", Green, White, screen, ConfirmMap)

        else:
            Finishedboxyaya = pygame.Rect(menuxy[0]+100, menuxy[1]+100, 500, 200)
            Button(Finishedboxyaya, "Finished! Start Game!", White, White, screen)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])