from UnipyEngine.Core import GameObject
from UnipyEngine.Utils import Debug

class Scene:
    def __init__(self, name):
        self.name = name
        self.objects = []

        SceneManager.AddScene(self)

    def AddObject(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)

    def RemoveObject(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def Clear(self):
        self.objects.clear()

class SceneManager:
    scenes = {}
    current_scene = None

    @staticmethod
    def AddScene(scene: Scene):
        SceneManager.scenes[scene.name] = scene

    @staticmethod
    def LoadScene(name: str):
        if name not in SceneManager.scenes:
            Debug.LogError(f"Scene '{name}' not found", isFatal = True)

        if SceneManager.current_scene:
            if SceneManager.current_scene.name == name:
                return

        # vider la scène courante
        GameObject.instances.clear()

        # charger la nouvelle
        SceneManager.current_scene = SceneManager.scenes[name]

        for obj in SceneManager.current_scene.objects:
            GameObject.instances.append(obj)

        Debug.LogSuccess(f"Scene '{name}' loaded successfully")

    @staticmethod
    def GetActiveScene():
        if(SceneManager.current_scene):
            return SceneManager.current_scene
        else:
            Debug.LogError("There is no active Scene", isFatal = True)
