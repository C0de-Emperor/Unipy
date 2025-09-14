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
    def LoadScripts(folder="Assets"):
        if not os.path.exists(folder):
            print(f"UnipyEngine: Scripts folder '{folder}' not found")
            return

        for file in os.listdir(folder):
            if file.endswith(".py"):
                path = os.path.join(folder, file)
                module_name = os.path.splitext(file)[0]

                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module

                try:
                    spec.loader.exec_module(module)
                    print(f"UnipyEngine : [{module_name}] loaded successfully")

                    # Injecter toutes les classes du module dans globals()
                    for name, obj in module.__dict__.items():
                        print(f"UnipyEngine : [{name}] loaded successfully")
                        if isinstance(obj, type):  # si c’est une classe
                            globals()[name] = obj

                except Exception as e:
                    print(f"UnipyEngine : Error loading {module_name} -> {e}")