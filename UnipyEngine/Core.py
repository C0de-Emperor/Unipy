from UnipyEngine.Utils import Vector3, Vector2
from UnipyEngine.Utils import Debug

class Component:
    def __init__(self, requiredComponents=None, gameObject=None):
        self.gameObject = gameObject
        self.requiredComponents = requiredComponents if requiredComponents else []

    def CompareTag(self, tag:str):
        assert isinstance(tag, str)
        return (tag in self.gameObject.tags)
    
    def Clone(self, new_gameObject):
        import copy
        clone = copy.deepcopy(self)   # clone "shallow"
        clone.gameObject = new_gameObject
        return clone

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"

class Transform(Component):
    def __init__(self, position:Vector3, rotation:Vector3, size:Vector2, gameObject=None):
        assert isinstance(position, Vector3)
        assert isinstance(rotation, Vector3)
        assert isinstance(size, Vector2)

        super().__init__(gameObject=gameObject)
        self.position = position
        self.rotation = rotation
        self.size = size

class GameObject:
    instances = []

    def __init__(self, name = "GameObject", tags = None, components = None, auto_add=False):
        assert isinstance(name, str)

        self.name = name
        self.tags = tags or []
        self.components = []

        if components:
            for component in components:
                component.gameObject = self  # On assigne ce GameObject au composant
                self.components.append(component)

            for component in components:
                for requiredComponent in component.requiredComponents:
                    if not any(isinstance(c, requiredComponent) for c in components):
                        raise AssertionError(f"{component} requires <{requiredComponent.__name__}> on GameObject(id={id(self)})")

        if auto_add:
            self.AddToScene()

    def AddToScene(self):
        """Ajoute cet objet dans la scène"""
        if self not in GameObject.instances:
            from UnipyEngine.SceneManagement import SceneManager

            for comp in self.components:
                if hasattr(comp, "Start"):
                    comp.Start()

            SceneManager.GetActiveScene().AddObject(self)

            if self not in GameObject.instances:
                GameObject.instances.append(self)

    def GetComponent(self, targetComponent) -> Component:
        assert Component in targetComponent.__bases__

        for component in self.components:
            if isinstance(component, targetComponent):
                return component
        return None

    def AddComponent(self, comp_class, *args, **kwargs):
        comp = comp_class(gameObject=self, *args, **kwargs)
        self.components.append(comp)
        return comp

    def Destroy(self):
        """Détruit cet objet et ses composants"""
        from UnipyEngine.SceneManagement import SceneManager

        for comp in self.components:
            if hasattr(comp, "OnDestroy"):
                comp.OnDestroy()

        self.components.clear()

        SceneManager.GetActiveScene().RemoveObject(self)
        if self in GameObject.instances:
            GameObject.instances.remove(self)


    @staticmethod
    def Instantiate(original, position=None, rotation=None, name=None):
        # Crée une nouvelle instance du GameObject
        new_obj = GameObject(name or original.name + " (Clone)")

        # Copier les composants
        for comp in original.components:
            comp_copy = comp.Clone(new_obj)
            new_obj.components.append(comp_copy)

        # appliquer position / rotation si demandé
        t = new_obj.GetComponent(Transform)
        if t:
            if position: t.position = position
            if rotation: t.rotation = rotation

        # enfin, on ajoute dans la scène
        new_obj.AddToScene()
        return new_obj
