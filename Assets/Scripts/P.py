from UnipyEngine.Core import Component, Transform, GameObject
from UnipyEngine.Physics2D import Collider2D, Raycast, RaycastHit2D
from UnipyEngine.Input import Input, KeyCode
from UnipyEngine.Utils import Debug, Vector2
from UnipyEngine.SceneManagement import SceneManager


from UnipyEngine.ModuleManagement import Script
file_Type = Script(__name__)

class S(Component):
    def __init__(self, gameObject:GameObject = None):
        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):
        if(Input.GetKeyDown(KeyCode.A)):
            SceneManager.LoadScene("Menu")
            #self.gameObject.GetComponent(Transform).position.x += 10
        if(Input.GetKeyDown(KeyCode.E)):
            SceneManager.LoadScene("Game")
            #self.gameObject.GetComponent(Transform).position.x -= 10
        if(Input.GetKeyDown(KeyCode.F)):
            raycast = Raycast(self.gameObject.GetComponent(Transform).position, Vector2.down(), 52)
            if raycast.hit:
                Debug.Log(raycast.hit.collider.gameObject.name)


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
