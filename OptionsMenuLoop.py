import pygame
from ButtonStuff import Button
import FileReader
import time

##Options menu.
def OptionsLoop():
    ## Initialisoidaan kaikki uudestaan koska on kyseessä uusi looppi. Tehdään kaikki uudestaan koska ei saada lähetettyä eteenpäin.
    clock = pygame.time.Clock()
    size = FileReader.Filereader("Config.txt", "ConfigSize")[0] ##Vaikka ton voi asettaa mielivaltasesti. Liian pieni arvo räjäyttää kaiken naamaan.
    screen = pygame.display.set_mode(size)
    gashunk = True
    Black = (0,0,0)
    White = (0xFF,0xFF,0xFF)
    Green = ((0,220,0))

    MaxFPS = FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0]
    tempMaxFPS = MaxFPS
    Resolution = FileReader.Filereader("Config.txt", "ConfigSize")[0]
    tempResolution = Resolution

    def QuitMenu():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def SetFPS(number):
        def ActuallySetFPS():
            nonlocal tempMaxFPS
            tempMaxFPS = number
        return ActuallySetFPS

    def SetResolution(ituple):
        def ActuallySetResolution():
            nonlocal tempResolution
            tempResolution = ituple
        return ActuallySetResolution

    def PrintOptionsToFile():
        string = "{\"Window Size X\" : " +str(tempResolution[0])+", \"Window Size Y\" : "+str(tempResolution[1])+", \"MaxFPS\" : "+str(tempMaxFPS)+"}"
        file = open("Config.txt", 'w')
        file.write(string)
        file.close()
        QuitMenu()

    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        menuxy = ((size[0]/2)-260 , (size[1]/2)-330)
        menubox = pygame.Rect(menuxy[0], menuxy[1],520, size[1] - menuxy[1]*2)
        confirmbutton = pygame.Rect(menuxy[0]+40, menuxy[1]+540, 200, 80)
        quitbutton = pygame.Rect(menuxy[0]+280, menuxy[1]+540, 200, 80)
        twentyfps = pygame.Rect(menuxy[0]+40, menuxy[1]+180, 200, 80)
        sixtyfps = pygame.Rect(menuxy[0]+40, menuxy[1]+300, 200, 80)
        hundtwentyfps = pygame.Rect(menuxy[0]+40, menuxy[1]+420, 200, 80)
        smallres = pygame.Rect(menuxy[0]+280, menuxy[1]+180, 200, 80)
        medres = pygame.Rect(menuxy[0]+280, menuxy[1]+300, 200, 80)
        bigres = pygame.Rect(menuxy[0]+280, menuxy[1]+420, 200, 80)
        currentsettingsbox = pygame.Rect(menuxy[0]+40, menuxy[1]+40, 440, 100)

        ##Piirto koodi. Ensiksi ruutu valkoiseksi. Sitte scheissea ruutuun. Kaiken pitäis mennä fillin alapuolelle.
        screen.fill(White)

        pygame.draw.rect(screen, Black, menubox, 3)

        ##Piirretään nappi käyttäen sitä varten tehtyä funktiota.
        ## Button function kutsu: Button(rect, text, ac, pc, screen, action=None):
        Button(confirmbutton, "Save Settings", Green, White, screen, 25, PrintOptionsToFile)
        Button(quitbutton, "Main Menu", Green, White, screen, 25, QuitMenu)
        Button(twentyfps, "20 FPS", Green, White, screen, 25, SetFPS(20))
        Button(sixtyfps, "60 FPS", Green, White, screen, 25, SetFPS(60))
        Button(hundtwentyfps, "120 FPS", Green, White, screen, 25, SetFPS(120))
        Button(smallres, "800x600", Green, White, screen, 25, SetResolution((800, 600)))
        Button(medres, "1024x768", Green, White, screen, 25, SetResolution((1024,768)))
        Button(bigres, "1280x1024", Green, White, screen, 25, SetResolution((1280,1024)))
        Button(currentsettingsbox, "FPS: " +str(MaxFPS)+ ", Resolution: " + str(Resolution), White, White, screen, 25)
        ##Huom. FPS muuttaminen *saattaa* räjäyttää asiat käsiin. Excercise caution.

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])