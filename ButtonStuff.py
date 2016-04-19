import pygame
import TextCenterer

def Button(rect, text, ac, pc, screen, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, ac, rect)

        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, pc, rect)

    pygame.draw.rect(screen, (0,0,0), rect, 3)

    text = TextCenterer.ButtonText(text, rect, (0,0,0))
    text.draw(screen)