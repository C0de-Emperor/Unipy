from UnipyEngine.Core import Component, Transform, GameObject, LayerMask
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
        if(Input.GetKeyDown(KeyCode.E)):
            SceneManager.LoadScene("Game")
        if(Input.GetKeyDown(KeyCode.F)):
            pos = self.gameObject.transform.position
            
            raycast = Raycast(pos, Vector2.down(), 100, layerMask=LayerMask(1))
            if raycast.hit:
                Debug.Log(f"Raycast hit: {raycast.hit.collider.gameObject.name}")
                Debug.Log(f"Distance: {raycast.hit.distance}")
                Debug.Log(f"Point: {raycast.hit.point}")
                Debug.Log(f"Normal: {raycast.hit.normal}")


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
