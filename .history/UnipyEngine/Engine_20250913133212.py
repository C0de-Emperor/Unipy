import os
import sys
import importlib

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "HIDE"
import pygame
screen = None

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

    @staticmethod
    def LoadScripts(scripts_folder="Scripts"):
        """
        Charge dynamiquement tous les modules du dossier Scripts/
        et expose leurs classes dans le namespace global.
        """
        scripts_path = os.path.abspath(scripts_folder)
        if scripts_path not in sys.path:
            sys.path.append(scripts_path)

        for file in os.listdir(scripts_path):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]  # sans .py
                module = importlib.import_module(module_name)
                globals().update(module.__dict__)  # expose les classes au global