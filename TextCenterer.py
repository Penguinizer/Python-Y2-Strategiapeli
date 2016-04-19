import pygame
import TextCenterer

class ButtonText(object):
    ##Käytetään tekstin printtaamiseen nappeihin.
    ##Perustuu raskaasti stack overflowsta löytyneeseen esimerkkiin.
    ##Huomattava muutos oli se että syötetään functiolle rect, sen sijaan että annetaan vaan sen koko/coordinaatit.
    ##Krediitit menee martineau:lle : http://stackoverflow.com/questions/32673965/pygame-blitting-center
    def __init__(self, text, targetrect, color):
        self.targetrect = targetrect
        self.color = color
        self.text = text
        self.x = targetrect.x
        self.y = targetrect.y
        self.w = targetrect.w
        self.h = targetrect.h

        pygame.font.init()
        font = pygame.font.SysFont("Calibri", 25, True, False)
        width, height = font.size(self.text)
        xoffset = (self.w-width) // 2
        yoffset = (self.h-height) // 2
        self.coords = (self.x+xoffset, self.y+yoffset)
        self.txt = font.render(text, True, color)

    def draw(self, screen):
        screen.blit(self.txt, self.coords)
