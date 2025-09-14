from UnipyEngine.Core import Component
from UnipyEngine.Input import Input, KeyCode
class S(Component):
    def __init__(self, gameObject = None):

        super().__init__(gameObject=gameObject, requiredComponents=[])

    def Update(self, dt):
        if(Input.GetKeyDown(KeyCode.A)):
            print("e")