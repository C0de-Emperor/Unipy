from UnipyEngine.Utils import Vector3, Vector2, Debug
from typing import Type, TypeVar, Optional, List, TYPE_CHECKING

T = TypeVar("T", bound="Component")

if TYPE_CHECKING:
    from UnipyEngine.Physics2D import Collider2D

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

    # --- Optional lifecycle callbacks ---
    def Start(self) -> None:
        """Called when the GameObject is added to the scene"""
        pass

    def Update(self, dt: float) -> None:
        """Called every frame before rendering"""
        pass

    def OnDestroy(self) -> None:
        """Called when the GameObject is destroyed"""
        pass

    def Render(self, screen) -> None:
        """Called during the rendering phase"""
        pass

    def RenderCollider(self, screen) -> None:
        """Called during the rendering phase for debug collider visualization"""
        pass

    # --- Physics callbacks ---
    def OnCollisionEnter(self, other: "Collider2D") -> None:
        """Called when a collision with another collider starts"""
        pass

    def OnCollisionExit(self, other: "Collider2D") -> None:
        """Called when a collision with another collider ends"""
        pass

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

    def __init__(self, name:str = "GameObject", tags:Optional[List[str]] = None, transform: Optional[Transform] = None, components: Optional[List[Type[Component]]] = None, static: bool = False, layer: int = 0, auto_add: bool = False):
        assert isinstance(name, str)

        self.name:str = name
        self.tags:List[str] = tags or []
        self.components: List[Type[Component]] = []
        self.static: bool = static
        self.layer: int = layer  # 0-31 pour 32 couches possibles
        
        # Initialiser le Transform
        if transform is None:
            Debug.LogError(f"Transfom required on GameObject(id={id(self)}, name='{self.name}')", isFatal=True)
        else:
            self.transform: Transform = transform
            self.transform.gameObject = self

        if components:
            for component in components:
                component.gameObject = self  # On assigne ce GameObject au composant
                self.components.append(component)
                if isinstance(component, Transform):
                    Debug.LogError(f"Transfom component on GameObject(id={id(self)}, name='{self.name}') must be unique and separate", isFatal=True)

            components.append(transform)
            for component in components:
                for requiredComponent in component.requiredComponents:
                    if not any(isinstance(c, requiredComponent) for c in components):
                        Debug.LogError(f"{component} requires <{requiredComponent.__name__}> on GameObject(id={id(self)}, name='{self.name}')", isFatal=True)

        if auto_add:
            self.AddToScene()

    def AddToScene(self) -> None:
        """Ajoute cet objet dans la scène"""
        if self not in GameObject.instances:
            for comp in self.components:
                comp.Start()

            GameObject.instances.append(self)

    def GetComponent(self, targetComponent:Type[T], silent: bool = False) -> Optional[T]:
        assert Component in targetComponent.__bases__

        if targetComponent is Transform:
            return self.transform

        for component in self.components:
            if isinstance(component, targetComponent):
                return component
        
        if not silent:
            Debug.LogWarning(f"Component {targetComponent.__name__} not found on GameObject(id={id(self)}, name='{self.name}')")
        return None

    def HasComponent(self, targetComponent:Type[Component]) -> bool:
        """Vérifie si le GameObject possède un composant sans générer de warning"""
        assert Component in targetComponent.__bases__

        if targetComponent is Transform:
            return True  # Transform est toujours présent

        for component in self.components:
            if isinstance(component, targetComponent):
                return True
        return False
        
    def AddComponent(self, comp_class: Type[Component], *args, **kwargs) -> Component:
        comp = comp_class(gameObject=self, *args, **kwargs)
        self.components.append(comp)
        return comp

    def Destroy(self) -> None:
        """Détruit cet objet et ses composants"""
        for comp in self.components:
            comp.OnDestroy()

        self.components.clear()

        if self in GameObject.instances:
            GameObject.instances.remove(self)

    @staticmethod
    def Instantiate(original: "GameObject", position: Optional[Vector3] = None, rotation: Optional[Vector3] = None, name: Optional[str] = None) -> "GameObject":
        # Crée une nouvelle instance du GameObject
        # Copier le Transform original
        transform_copy = original.transform.Clone(None)
        
        # Créer le nouveau GameObject avec le Transform copié
        new_obj = GameObject(name or original.name + " (Clone)", transform=transform_copy)

        # Copier les autres composants (sauf Transform qui est déjà géré)
        for comp in original.components:
            if not isinstance(comp, Transform):
                comp_copy = comp.Clone(new_obj)
                new_obj.components.append(comp_copy)

        # appliquer position / rotation si demandé
        if position: new_obj.transform.position = position
        if rotation: new_obj.transform.rotation = rotation

        # enfin, on ajoute dans la scène
        new_obj.AddToScene()
        return new_obj

class LayerMask:
    """Masque de couches pour filtrer les collisions et raycasts."""
    def __init__(self, mask: int = 0) -> None:
        self.mask: int = mask

    def __or__(self, other: "LayerMask") -> "LayerMask":
        """Combine deux LayerMask avec OR"""
        if isinstance(other, int):
            return LayerMask(self.mask | other)
        return LayerMask(self.mask | other.mask)

    def __ror__(self, other: int) -> "LayerMask":
        """Combine deux LayerMask avec OR (right operand)"""
        return LayerMask(self.mask | other)

    def __and__(self, other: "LayerMask") -> bool:
        """Teste si deux LayerMask ont des couches en commun"""
        if isinstance(other, int):
            return bool(self.mask & other)
        return bool(self.mask & other.mask)

    def __rand__(self, other: int) -> bool:
        """Teste si deux LayerMask ont des couches en commun (right operand)"""
        return bool(self.mask & other)

    @staticmethod
    def GetMask(*layer_names: str) -> "LayerMask":
        """Crée un LayerMask à partir de noms de couches."""
        mask = 0
        for name in layer_names:
            if name in LayerMask.LAYER_NAMES:
                mask |= (1 << LayerMask.LAYER_NAMES[name])
        return LayerMask(mask)

    @staticmethod
    def NameToLayer(name: str) -> int:
        """Convertit un nom de couche en numéro."""
        return LayerMask.LAYER_NAMES.get(name, 0)

    @staticmethod
    def LayerToName(layer: int) -> str:
        """Convertit un numéro de couche en nom."""
        for name, num in LayerMask.LAYER_NAMES.items():
            if num == layer:
                return name
        return "Unknown"

    # Noms de couches prédéfinis (peuvent être étendus)
    LAYER_NAMES: dict[str, int] = {
        "Default": 0,
        "Player": 1,
        "Enemy": 2,
        "Ground": 3,
        "Obstacle": 4,
        "Projectile": 5,
        "UI": 6,
        "Water": 7,
        "Air": 8,
    }

    def __str__(self) -> str:
        return f"LayerMask({bin(self.mask)})"

    def __repr__(self) -> str:
        return f"LayerMask({self.mask})"