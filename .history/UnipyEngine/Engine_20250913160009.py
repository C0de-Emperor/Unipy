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

    def GenerateAssetsInit():
        """Génère automatiquement le __init__.py dans Assets/"""
        files = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py") and f != "__init__.py"]
        lines = [f"from .{os.path.splitext(f)[0]} import *\n" for f in files]
        
        init_path = os.path.join(SCRIPTS_FOLDER, "__init__.py")
        with open(init_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def LoadScripts():
        """Charge dynamiquement les scripts et détecte les nouveaux fichiers"""
        global loaded_scripts
        if not os.path.exists(SCRIPTS_FOLDER):
            print(f"UnipyEngine: Scripts folder '{SCRIPTS_FOLDER}' not found")
            return False

        current_files = set(f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py"))
        new_files = current_files - loaded_scripts

        if new_files:
            print("UnipyEngine: New scripts detected, regenerating __init__.py...")
            GenerateAssetsInit()
            print("UnipyEngine: Reloading complete, stop current run to prevent errors.")
            loaded_scripts.update(current_files)
            return False  # stop le run pour ce cycle
        else:
            # charger les modules existants
            for file in current_files:
                if file.endswith(".py"):
                    module_name = os.path.splitext(file)[0]
                    path = os.path.join(SCRIPTS_FOLDER, file)
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
            return True