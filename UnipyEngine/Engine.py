import os
import sys
import time
import re
import pygame

from UnipyEngine.Input import Input
from UnipyEngine.Physics import Rigidbody2D
from UnipyEngine.Utils import Debug, Color

screen = None

class Engine:
    screen = None
    static_screen = None
    color = None
    clock = None
    running = False
    renderCollider = False

    @staticmethod
    def Init(width=800, height=800, color:Color = Color(0, 0, 0), renderCollider = False):
        pygame.init()
        Engine.screen = pygame.display.set_mode((width, height))
        Engine.static_screen = pygame.Surface((width, height))
        Engine.renderCollider = renderCollider

        Engine.clock = pygame.time.Clock()
        Engine.running = True
        Engine.color = color
        Engine.screen.fill((color.r, color.g, color.b))
        Engine.static_screen.fill((color.r, color.g, color.b))
        pygame.display.flip()
        
    @staticmethod
    def BakeStaticObjects():
        from UnipyEngine.Core import GameObject
        # Créer une surface monde pour les statiques (assez grande pour le monde)
        Engine.static_world_surface = pygame.Surface((10000, 10000), pygame.SRCALPHA)
        Engine.static_world_surface.fill((0, 0, 0, 0))  # transparent

        for gameObject in GameObject.instances:
            if gameObject.static:
                for comp in gameObject.components:
                    if hasattr(comp, "Render") and callable(comp.Render):
                        # Rendre en coordonnées monde sur static_world_surface
                        comp.Render(Engine.static_world_surface)
                if Engine.renderCollider:
                    for comp in gameObject.components:
                        if hasattr(comp, "RenderCollider") and callable(comp.RenderCollider):
                            comp.RenderCollider(Engine.static_world_surface)


    @staticmethod
    def Run():
        from UnipyEngine.Core import GameObject, Vector3, Transform
        Engine.BakeStaticObjects()

        while Engine.running:
            Rigidbody2D.ClearFrameCollisions()

            Engine.screen.fill((Engine.color.r, Engine.color.g, Engine.color.b))
            # Blitter la surface statique optimisée
            from UnipyEngine.Rendering import Camera
            if Camera.active_camera and Engine.static_world_surface:
                cam = Camera.active_camera
                zoom = cam.zoom
                # Position écran pour (0,0) monde (centre)
                screen_00 = Camera.WorldToScreen(Vector3(0, 0, 0))
                if zoom == 1.0:
                    # Pas de scaling pour zoom=1, plus rapide
                    Engine.screen.blit(Engine.static_world_surface, (screen_00.x, screen_00.y))
                else:
                    # Scaling pour autres zooms (plus lent)
                    scaled_static = pygame.transform.scale(Engine.static_world_surface, (int(10000 * zoom), int(10000 * zoom)))
                    Engine.screen.blit(scaled_static, (screen_00.x, screen_00.y))
            dt = Engine.clock.tick(60) / 1000.0

            events = pygame.event.get()
            Input.UpdateEvents(events)  # mise à jour des inputs

            # 1) Update: appeler Update sur TOUS les composants avant de renderer.
            for gameObject in GameObject.instances:
                for component in gameObject.components:
                    if hasattr(component, "Update") and callable(component.Update):
                        component.Update(dt)

            # 2) Render: renderiser tous les objets non-statiques après les updates
            for gameObject in GameObject.instances:
                if not gameObject.static:
                    for component in gameObject.components:
                        if hasattr(component, "Render") and callable(component.Render):
                            component.Render(Engine.screen)
                    if Engine.renderCollider:
                        for comp in gameObject.components:
                            if hasattr(comp, "RenderCollider") and callable(comp.RenderCollider):
                                comp.RenderCollider(Engine.screen)

            pygame.display.flip()

            for event in events:
                if event.type == pygame.QUIT:
                    Engine.running = False

        print("")
        Debug.LogSuccess("Exit")
        print("")
        pygame.quit()

    @staticmethod
    def is_valid_module_name(filename: str) -> bool:
        """Vérifie si le nom de fichier correspond à un identifiant Python valide."""
        name = os.path.splitext(filename)[0]
        return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None
    
    @staticmethod
    def LoadScripts(folder="Assets"):
        # nettoyer la console
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.5)

        if not os.path.exists(folder):
            Debug.LogError(f"UnipyEngine: Scripts folder '{folder}' not found", isFatal=True)
            
        init_file = os.path.join(folder, "__init__.py")

        # 1. récupérer les scripts connus
        known_files = set()
        if os.path.exists(init_file):
            with open(init_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("from .") and " import *" in line:
                        parts = line.split()[1].lstrip(".").split(".")
                        known_files.add(".".join(parts))

        # 2. récupérer les scripts actuels récursivement
        current_files = set()
        for root, dirs, files in os.walk(folder):
            rel_root = os.path.relpath(root, folder)
            if rel_root == '.':
                rel_root = ''
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module_name = os.path.splitext(file)[0]
                    if Engine.is_valid_module_name(file):
                        dotted_path = rel_root.replace(os.sep, '.') + ('.' if rel_root else '') + module_name
                        current_files.add(dotted_path)

        # 3. comparer
        added = current_files - known_files
        removed = known_files - current_files

        if added or removed:
            hasInvalidMod = False

            # affichage clair
            Debug.LogWarnig("UnipyEngine: Scripts changed, reloading required.\n")
            time.sleep(0.5)
            for mod in sorted(added):
                file = f"{mod.replace('.', os.sep)}.py"
                Debug.LogSuccess(f"   + {file}")
                time.sleep(0.5)
            for mod in sorted(removed):
                file = f"{mod.replace('.', os.sep)}.py"
                Debug.LogSuccess(f"   - {file}")
                time.sleep(0.5)

            # régénérer les __init__.py
            # First, collect all modules per directory
            all_modules = {}
            for root, dirs, files in os.walk(folder):
                rel_root = os.path.relpath(root, folder)
                if rel_root == '.':
                    rel_root = ''
                modules_in_dir = []
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        module_name = os.path.splitext(file)[0]
                        if Engine.is_valid_module_name(file):
                            modules_in_dir.append(module_name)
                        else:
                            hasInvalidMod = True
                if modules_in_dir:
                    all_modules[rel_root] = modules_in_dir

            # Generate __init__.py for each directory with modules
            for rel_dir, modules in all_modules.items():
                dir_path = os.path.join(folder, rel_dir) if rel_dir else folder
                init_path = os.path.join(dir_path, '__init__.py')
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write("# Auto-generated by UnipyEngine.Engine\n")
                    for mod in sorted(modules):
                        f.write(f"from .{mod} import *\n")

            # For the main __init__.py, also import all modules from subdirs
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("# Auto-generated by UnipyEngine.Engine\n")
                # Import local modules
                if '' in all_modules:
                    for mod in sorted(all_modules['']):
                        f.write(f"from .{mod} import *\n")
                # Import modules from subdirs
                for rel_dir, modules in sorted(all_modules.items()):
                    if rel_dir:  # not root
                        for mod in modules:
                            dotted_path = rel_dir.replace(os.sep, '.')
                            f.write(f"from .{dotted_path}.{mod} import *\n")

            if hasInvalidMod:
                print("\n")
                Debug.LogError("Module names must contain only letters, numbers and '_'\n")

            # petit délai pour lisibilité + arrêt du run
            time.sleep(1)
            Debug.LogSuccess("UnipyEngine: Reloading complete. Please restart.")
            sys.exit(0)
        else:
            Debug.LogSuccess("Loading Complete\n")
            time.sleep(0.5)

