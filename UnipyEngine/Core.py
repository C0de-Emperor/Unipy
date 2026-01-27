from UnipyEngine.Utils import Vector3, Vector2, Debug
from typing import Type, TypeVar, Optional, List

T = TypeVar("T", bound="Component")

from typing import Optional, List, Type

class Component:
    def __init__(self, requiredComponents: Optional[List[Type["Component"]]] = None, gameObject: Optional["GameObject"] = None):
        self.gameObject: Optional["GameObject"] = gameObject
        self.requiredComponents: List[Type["Component"]] = requiredComponents if requiredComponents is not None else []

    def CompareTag(self, tag:str) -> bool:
        assert isinstance(tag, str)
        return (tag in self.gameObject.tags)
    
    def Clone(self, new_gameObject:"GameObject"):
        import copy
        clone = copy.deepcopy(self)   # clone "shallow"
        clone.gameObject = new_gameObject
        return clone

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"

class Transform(Component):
    def __init__(self, position:Vector3, rotation:Vector3, size:Vector2, gameObject:Optional["GameObject"] = None):
        assert isinstance(position, Vector3)
        assert isinstance(rotation, Vector3)
        assert isinstance(size, Vector2)

        super().__init__(gameObject=gameObject)
        self.position: Vector3 = position
        self.rotation: Vector3 = rotation
        self.size: Vector2 = size

class GameObject:
    instances: List["GameObject"] = []

    def __init__(self, name:str = "GameObject", tags:Optional[List[str]] = None, components: Optional[List[Type[Component]]] = None, static: bool = False, auto_add: bool = False):
        assert isinstance(name, str)

        self.name:str = name
        self.tags:List[str] = tags or []
        self.components: List[Type[Component]] = []
        self.static: bool = static

        if components:
            for component in components:
                component.gameObject = self  # On assigne ce GameObject au composant
                self.components.append(component)

            for component in components:
                for requiredComponent in component.requiredComponents:
                    if not any(isinstance(c, requiredComponent) for c in components):
                        Debug.LogError(f"{component} requires <{requiredComponent.__name__}> on GameObject(id={id(self)})", isFatal=True)
        else:
            pass

        if auto_add:
            self.AddToScene()

    def AddToScene(self) -> None:
        """Ajoute cet objet dans la scène"""
        if self not in GameObject.instances:
            for comp in self.components:
                if hasattr(comp, "Start"):
                    comp.Start()

            GameObject.instances.append(self)

    def GetComponent(self, targetComponent:Type[T]) -> Optional[T]:
        assert Component in targetComponent.__bases__

        for component in self.components:
            if isinstance(component, targetComponent):
                return component
        return None

    def AddComponent(self, comp_class: Type[Component], *args, **kwargs) -> Component:
        comp = comp_class(gameObject=self, *args, **kwargs)
        self.components.append(comp)
        return comp

    def Destroy(self) -> None:
        """Détruit cet objet et ses composants"""
        for comp in self.components:
            if hasattr(comp, "OnDestroy"):
                comp.OnDestroy()

        self.components.clear()

        if self in GameObject.instances:
            GameObject.instances.remove(self)

    @staticmethod
    def Instantiate(original: "GameObject", position: Optional[Vector3] = None, rotation: Optional[Vector3] = None, name: Optional[str] = None) -> "GameObject":
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
