from UnipyEngine.Core import Component, GameObject
from UnipyEngine.Physics import Collider2D
from UnipyEngine.Input import Input, KeyCode
from UnipyEngine.Utils import Debug
from UnipyEngine.SceneManagement import SceneManager


class S(Component):
    def __init__(self, gameObject = None):
        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):
        if(Input.GetKeyDown(KeyCode.A)):
            SceneManager.LoadScene("Menu")
        if(Input.GetKeyDown(KeyCode.E)):
            SceneManager.LoadScene("Game")

    def Start(self):
        #Debug.Log("created")
        pass

    def OnCollisionEnter(self, other:Collider2D):
        #Debug.Log(self.gameObject.name + " enter collide " + other.gameObject.name)
        #GameObject.Destroy(self.gameObject)
        pass

    def OnCollisionExit(self, other:Collider2D):
        pass
        #Debug.Log(self.gameObject.name + " exit collide " + other.gameObject.name)
