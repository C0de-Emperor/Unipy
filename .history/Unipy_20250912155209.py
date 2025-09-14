import math



class PathError(Exception):
    def __init__(self, message:str):
        self.message = message



CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)  # parent du fichier

if(os.path.exists(os.path.join(CURRENT_DIR, "Assets"))):
    ASSETS_FOLDER_DIR = os.path.join(CURRENT_DIR, "Assets")
else:
    raise PathError(f"Assets folder does not exist at : {CURRENT_DIR}")

if(os.path.exists(os.path.join(CURRENT_DIR, "Scripts"))):
    SCRIPTS_FOLDER_DIR = os.path.join(CURRENT_DIR, "Scripts")
else:
    raise PathError(f"Scripts folder does not exist at : {CURRENT_DIR}")














gm1 = GameObject([
        Transform(Vector3(110, 40, 0), Vector3(0, 0, 0), Vector2(30, 30)),
        SpriteRenderer(DrawingShape.CIRCLE, Color(20, 140, 30)),
        Rigidbody2D(Vector2(5, 0), BodyState.CYNEMATIC , mass=2),
        CircleCollider2D(15)
    ])

gm2 = GameObject([
        Transform(Vector3(110, 440, 0), Vector3(0, 0, 0), Vector2(100, 100)),
        SpriteRenderer(DrawingShape.SQUARE, Color(200, 200, 30)),
        Rigidbody2D(Vector2(0, -10), BodyState.KYNEMATIC , mass=2),
        BoxCollider2D(Vector2(100, 100))
    ])

#gm.GetComponent(Rigidbody2D).AddForce(Vector2(200000, -200000))

"""

"""





"""
print(tr)
print(type(tr))
print(type(tr).__bases__[0])
"""