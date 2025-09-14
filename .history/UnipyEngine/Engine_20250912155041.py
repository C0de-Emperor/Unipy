import os
from UnipyEngine.Core import GameObject # type: ignore

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "HIDE"
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800), ) #pygame.RESIZABLE

screen.fill((0, 0, 0))
pygame.display.flip()

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    dt = clock.tick(60) / 1000.0  # secondes écoulées depuis la dernière frame

    # On appelle Update sur chaque composant qui le possède
    for gameObject in GameObject.instances:
        for component in gameObject.components:
            if hasattr(component, "Update") and callable(component.Update):
                component.Update(dt)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()