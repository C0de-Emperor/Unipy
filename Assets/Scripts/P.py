from UnipyEngine.Core import Component
from UnipyEngine.Physics import Collider2D
from UnipyEngine.Input import Input, KeyCode
from UnipyEngine.Utils import Debug
from UnipyEngine.SceneManagement import SceneManager


from UnipyEngine.ModuleManagement import Script
file_Type = Script(__name__)

class S(Component):
    def __init__(self, gameObject = None):
        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):

        if(Input.GetKeyDown(KeyCode.A)):
            SceneManager.LoadScene("Menu")
            Debug.Log("A pressed")
            #self.gameObject.GetComponent(Transform).position.x += 10
        if(Input.GetKeyDown(KeyCode.E)):
            SceneManager.LoadScene("Game")
            #self.gameObject.GetComponent(Transform).position.x -= 10

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
