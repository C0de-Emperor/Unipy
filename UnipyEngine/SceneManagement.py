from UnipyEngine.Core import GameObject
from UnipyEngine.Utils import Debug
from UnipyEngine.ModuleManagement import ModuleManager


class SceneManager:
    current_scene = None

    @staticmethod
    def LoadScene(name: str):
        if SceneManager.current_scene == name:
            return

        # vider la scène courante
        GameObject.instances.clear()

        # charger la nouvelle scène en appelant la fonction load() du module de scène
        try:
            scene_module = ModuleManager.find_module("scene", name)
            if scene_module and hasattr(scene_module, 'load'):
                scene_module.load()
                SceneManager.current_scene = name
                # Recréer la surface statique avec les nouveaux objets
                from UnipyEngine.Engine import Engine
                Engine.BakeStaticObjects()
                Debug.LogSuccess(f"Scene '{name}' loaded successfully")
            else:
                Debug.LogError(f"Scene '{name}' not found or does not have a load() function", isFatal=True)
        except Exception as e:
            Debug.LogError(f"Error loading scene '{name}': {e}", isFatal=True)

    @staticmethod
    def GetActiveScene():
        return SceneManager.current_scene
