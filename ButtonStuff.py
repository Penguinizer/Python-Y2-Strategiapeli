import pygame
import TextCenterer
import time

def Button(rect, text, ac, pc, screen, fontsize, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, ac, rect)

        if click[0] == 1 and action != None:
            action()
            time.sleep(0.1)

    else:
        pygame.draw.rect(screen, pc, rect)

    pygame.draw.rect(screen, (0,0,0), rect, 3)

    text = TextCenterer.ButtonText(text, rect, (0,0,0), fontsize)
    text.draw(screen)