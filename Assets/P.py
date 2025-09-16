from UnipyEngine.Core import Component, GameObject
from UnipyEngine.Physics import Collider2D
from UnipyEngine.Input import Input, KeyCode
from UnipyEngine.Utils import Debug


class S(Component):
    def __init__(self, gameObject = None):

        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):
        if(Input.GetKeyDown(KeyCode.A)):
            print("e")

    def Start(self):
        Debug.Log("created")

    def OnCollisionEnter(self, other:Collider2D):
        #Debug.Log(self.gameObject.name + " enter collide " + other.gameObject.name)
        #GameObject.Destroy(self.gameObject)
        pass

    def OnCollisionExit(self, other:Collider2D):
        pass
        #Debug.Log(self.gameObject.name + " exit collide " + other.gameObject.name)
