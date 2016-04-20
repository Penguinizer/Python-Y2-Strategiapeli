import pygame
import FileReader
import TextCenterer
from ButtonStuff import Button
from OptionsMenuLoop import OptionsLoop

def mainmenu():
    '''
    Periaatteessa tämän pitäis olla main menu. Tästä sitten kutsutaan toisia funktioita joilla on omat loopit.
     Esim. Options menu, game setup (joka vuorostaan kutsuu pää peli funktion).
     Alla random setup roinaa.
    '''
    pygame.init()
    clock = pygame.time.Clock()
    size = FileReader.Filereader("Config.txt", "ConfigSize")[0] ##Vaikka ton voi asettaa mielivaltasesti. Liian pieni arvo räjäyttää kaiken naamaan.
    screen = pygame.display.set_mode(size)
    gashunk = True
    ##Definetaan päänsäryn välttämiseksi.
    Black = (0,0,0)
    White = (0xFF,0xFF,0xFF)
    Green = ((0,220,0))

    def QuitGame():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while gashunk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Peli sulkeutuu painamalla closea.
                gashunk = False

        ##Rectit määritellään tässä. Pitää määritellä tässä koska muuten pelilogiikan hiiri osio ei toimi oikein.
        menuxy = ((size[0]/2)-200, (size[1]/2)-180)
        titlebox = pygame.Rect(menuxy[0], menuxy[1]-100, 400, 80)
        menubox = pygame.Rect(menuxy[0], menuxy[1],400,460)
        startgamebutton = pygame.Rect(menuxy[0]+40, menuxy[1]+40, 320, 100)
        optionsbutton = pygame.Rect(menuxy[0]+40, menuxy[1]+180, 320, 100)
        quitbutton = pygame.Rect(menuxy[0]+40, menuxy[1]+320, 320, 100)

        ##Pelilogiikka scheisse tähän väliin.

        ##Piirto koodi. Ensiksi ruutu valkoiseksi. Sitte scheissea ruutuun. Kaiken pitäis mennä fillin alapuolelle.
        screen.fill(White)

        ##Piirretään valkoinen rect menuboxin alle. Tämä on siksi jos joskus lisään taustalle jotain.
        ##Piirretään myös ei-nappi rectit.
        pygame.draw.rect(screen, White, titlebox)
        pygame.draw.rect(screen, White, menubox)
        pygame.draw.rect(screen, Black, titlebox, 3)
        pygame.draw.rect(screen, Black, menubox, 3)

        ##Teksti roinat vakio rect:eissä.
        title = TextCenterer.ButtonText("Python-Y2 Strategy Game", titlebox, Black)
        title.draw(screen)

        ##Piirretään nappi käyttäen sitä varten tehtyä funktiota.
        ## Button function kutsu: Button(rect, text, ac, pc, screen, action=None):
        Button(startgamebutton, "Start Game", Green, White, screen)
        Button(optionsbutton, "Options", Green, White, screen, OptionsLoop)
        Button(quitbutton, "Quit Game", Green, White, screen, QuitGame)

        ##Updatettaa ruudun ainaki guiden mukaan. Ruudun piirto tämän yläpuolelle.
        pygame.display.flip()
        ##Asetetaan max FPS config tiedoston mukaan.
        clock.tick(FileReader.Filereader("Config.txt", "ConfigMaxFPS")[0])

    pygame.quit()

mainmenu()