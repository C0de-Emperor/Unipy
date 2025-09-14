from UnipyEngine.Utils import Vector3, Vector2


class Component:
    def __init__(self, requiredComponents=None, gameObject=None):
        self.gameObject = gameObject
        self.requiredComponents = requiredComponents if requiredComponents else []

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
    def __init__(self, components):
        GameObject.instances.append(self)
        self.components = []
        for component in components:
            component.gameObject = self  # On assigne ce GameObject au composant
            self.components.append(component)

        for component in components:
            for requiredComponent in component.requiredComponents:
                if not any(isinstance(c, requiredComponent) for c in components):
                    raise AssertionError(f"{component} requires <{requiredComponent.__name__}> on GameObject(id={id(self)})")

    def GetComponent(self, targetComponent) -> Component:
        assert Component in targetComponent.__bases__

        for component in self.components:
            if isinstance(component, targetComponent):
                return component
        return None
