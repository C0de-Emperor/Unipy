from UnipyEngine import *
from Assets import *

# Charge tous les scripts custom
Engine.LoadScripts("Assets")

Engine.Init(800, 800)

# Définition des scènes
game = Scene("Game")
menu = Scene("Menu")
SceneManager.LoadScene("Game")

"""
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
"""

tileset = {
    0 : Color(200, 0, 0),
    1 : Color(0, 200, 0),
    2 : Color(0, 0, 200)
}

tilemap = GameObject(
    name = "Tilemap",
    tags = [],
    components= [
        Transform(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector2(0, 0)),
        TilemapRenderer(Vector2(50, 50), r"Assets\Tilemap.json", tileset=tileset)
    ],
    auto_add = True
)

Engine.Run()

