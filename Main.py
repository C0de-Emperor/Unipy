from UnipyEngine import *
from Assets import *
import time

# Charge tous les scripts custom
Engine.LoadScripts("Assets")

Engine.Init(800, 800)

# Définition des scènes
game = Scene("Game")
menu = Scene("Menu")
SceneManager.LoadScene("Game")

ball = GameObject(
    name = "Ball 1",
    tags = [
        "Ball b"
    ],
    components= [
        Transform(Vector3(100, 100, 0), Vector3(0, 0, 0), Vector2(30, 30)),
        SpriteRenderer(DrawingShape.CIRCLE, Color(0, 255, 0)),
        Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1),
        CircleCollider2D(15),
        P.S()
    ],
    auto_add = False
)

GameObject.Instantiate(ball, position= Vector3(10, 10, 0), name = 'ball 1')
GameObject.Instantiate(ball, position= Vector3(60, 40, 0), name = 'ball 2')
GameObject.Instantiate(ball, position= Vector3(100, 200, 0), name = 'ball 3')

menu.AddObject(ball)



"""
GameObject(
    "Ball 2",
    [
        "Ball v"
    ],
    [
        Transform(Vector3(110, 40, 0), Vector3(0, 0, 0), Vector2(30, 30)),
        SpriteRenderer(DrawingShape.CIRCLE, Color(20, 140, 30)),
        Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC , mass=200),
        CircleCollider2D(15),
        
    ]
)
"""


GameObject(
    name = "Cube",
    tags = [
        "Cube"
    ],
    components = [
        Transform(Vector3(110, 440, 0), Vector3(0, 0, 0), Vector2(100, 100)),
        SpriteRenderer(DrawingShape.SQUARE, Color(200, 200, 30)),
        Rigidbody2D(Vector2(0, 0), BodyState.KINEMATIC , mass=20),
        BoxCollider2D(Vector2(100, 100))
    ],
    auto_add = False
).AddToScene()



Engine.Run()

