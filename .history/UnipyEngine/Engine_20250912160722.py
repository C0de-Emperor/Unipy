import os
from UnipyEngine.Core import GameObject

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "HIDE"
import pygame

import pygame

class Engine:
    screen = None
    clock = None
    running = False

    @staticmethod
    def Init(width=800, height=800):
        pygame.init()
        Engine.screen = pygame.display.set_mode((width, height))
        Engine.clock = pygame.time.Clock()
        Engine.running = True
        Engine.screen.fill((0, 0, 0))
        pygame.display.flip()

    @staticmethod
    def Run():
        from UnipyEngine.Core import GameObject  # éviter import circulaire

        while Engine.running:
            Engine.screen.fill((0, 0, 0))
            dt = Engine.clock.tick(60) / 1000.0

            # update des GameObjects
            for gameObject in GameObject.instances:
                for component in gameObject.components:
                    if hasattr(component, "Update") and callable(component.Update):
                        component.Update(dt)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Engine.running = False

        pygame.quit()

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