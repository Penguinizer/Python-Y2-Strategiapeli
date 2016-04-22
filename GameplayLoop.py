import FileReader
import pygame
import math
from ButtonStuff import Button

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
    xmapscrollvar = 0
    ymapscrollvar = 0

    '''
    Testiroinaa:
    for player in Game.Players:
        for unit in player.PlayerUnitList:
            print(unit.Name)
            print(unit.Equipment)
    '''

    def QuitGame():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def MapScrollUp():
        nonlocal ymapscrollvar
        if ymapscrollvar < ymax-1:
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
        if xmapscrollvar < xmax-1:
            xmapscrollvar += 1

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

        ##Map scroll napit.
        Nbutton = pygame.Rect(size[0]-175, size[1]-175, 75, 75)
        Wbutton = pygame.Rect(size[0]-250, size[1]-100, 75, 75)
        Sbutton = pygame.Rect(size[0]-175, size[1]-100, 75, 75)
        Ebutton = pygame.Rect(size[0]-100, size[1]-100, 75, 75)
        Button(Nbutton, "N", Green, White, screen, MapScrollDown)
        Button(Wbutton, "W", Green, White, screen, MapScrollLeft)
        Button(Sbutton, "S", Green, White, screen, MapScrollUp)
        Button(Ebutton, "E", Green, White, screen, MapScrollRight)

        ##Komentonapit.

        ##Roina
        Button(pygame.Rect(100*xmapscrollvar, 100*ymapscrollvar, 100, 100), "Test", Green, White, screen)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])