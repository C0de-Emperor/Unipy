from UnipyEngine.Core import Component
from UnipyEngine.Physics import Collider2D
from UnipyEngine.Input import Input, KeyCode


class S(Component):
    def __init__(self, gameObject = None):

        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):
        if(Input.GetKeyDown(KeyCode.A)):
            print("e")

    def OnCollisionEnter(self, other:Collider2D):
        if(other.CompareTag("Ball b")):
            print(self.gameObject.name + " enter collide Ball 1")
        if(other.CompareTag("Cube")):
            print(self.gameObject.name + " enter collide Cude")

    def OnCollisionExit(self, other:Collider2D):
        if(other.CompareTag("Ball b")):
            print(self.gameObject.name + " exit collide Ball 1")
        if(other.CompareTag("Cube")):
            print(self.gameObject.name + " exit collide Cude")
        