from UnipyEngine.Core import GameObject
from UnipyEngine.Utils import Debug

class SceneManager:
    current_scene: str = None

    @staticmethod
    def LoadScene(name: str) -> None:
        from UnipyEngine.Rendering import Camera
        if SceneManager.current_scene == name:
            return

        # vider la scène courante
        GameObject.instances.clear()
        Camera.active_camera = None

        # charger la nouvelle scène en appelant la fonction load() du module de scène
        try:
            from UnipyEngine.ModuleManagement import ModuleType
            scene_obj = ModuleType.registry.get(("scene", name))
            if scene_obj and hasattr(scene_obj, 'load_func'):

                scene_obj.load_func()
                SceneManager.current_scene = name

                # Recréer la surface statique avec les nouveaux objets
                from UnipyEngine.Engine import Engine
                Engine.BakeStaticObjects()
                Debug.LogSuccess(f"Scene '{name}' loaded successfully")
            else:
                Debug.LogError(f"Scene '{name}' not found or does not have a valid scene object with load_func", isFatal=True)
        except Exception as e:
            Debug.LogError(f"Error loading scene '{name}': {e}", isFatal=True)

    @staticmethod
    def LoadInitialScene() -> None:
        import os, json
        if not os.path.exists(r"Settings.json"):
            Debug.LogError(f"No 'Settings.json' file", isFatal=True)
            return
        with open(r'Settings.json', 'r', encoding='utf-8') as fichier:
            settings = json.load(fichier)
            SceneManager.LoadScene(settings["initialScene"])
            del settings

    @staticmethod
    def GetActiveScene() -> str:
        return SceneManager.current_scene
